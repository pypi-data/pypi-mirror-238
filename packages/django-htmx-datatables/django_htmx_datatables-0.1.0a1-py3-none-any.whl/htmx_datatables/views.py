"""Data table generic views."""

from enum import Enum
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import unquote

from django.core.exceptions import (
    FieldDoesNotExist,
    FieldError,
    ImproperlyConfigured,
    ObjectDoesNotExist,
)
from django.db import models
from django.db.models import Q, Sum
from django.utils.decorators import method_decorator
from django.utils.html import conditional_escape
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import ListView

from .core import Column, ColumnFormatter, Columns, DataCell, DataRow
from .helpers import add_enum_to_context, camel_to_snake

# Current

# Planned
# TODO: Support ordering by multiple columns
# TODO: Add localization
# TODO: Adjust width of filter widgets automatically


class QueryParam(str, Enum):
    """A URL query param supported by HtmxDataTableView."""

    DARK_MODE = "dm"  # Dark mode enabled (when True) else disabled
    FILTER_PREFIX = "f_"  # Prefix of a filter param
    ORDER_BY = "o"  # Sort by column given as index
    PAGE = "p"  # Page numbers
    PAGINATE_BY = "n"  # Current maximum count of entries shown
    SEARCH = "q"  # Filter search fields by matching search string
    SUBVIEW = "v"  # Subview, e.g. main or filter


class _SubView(str, Enum):
    """A sub view supported by HtmxDataTableView.."""

    MAIN = "main"
    FILTER = "filter"
    DATA = "data"


class HtmxDataTableView(ListView):
    """Generic class for creating htmx data table views.

    The only mandatory configurations are to define ``columns`` and a queryset.
    A queryset can be defined via the class properties ``model`` or ``queryset``
    or by overriding the method ``get_initial_queryset()``.

    For additional features & configuration please see comments below and ``ListView``.

    Raises ``ImproperlyConfigured`` when there is a configuration error.

    The example definition looks like this:

    .. code-block:: python

        class BookDataTableView(DataTableView):
            model = Book
            columns = ["name"]

    """

    columns: List[str] = []
    """Columns to be rendered. Mandatory.

    Can be the name of a field on the model or method for rendering the column.
    Can also be a tuple consisting of name and label.

    Note that stringy results of a render method are always escaped, unless marked as safe.
    """

    format_columns: Dict[str, str] = {}

    filters: List[str] = []
    """Show filter drop downs for specified fields. Optional.

    Example: ``filters = ["field_1", "field_2", ...]``

    Needs to be valid field on the Django object of the related queryset (i.e. a mode field or annotated).

    By default the name of the filter is derived from the field name. Alternatively, a custom label can be defined

    Example: ``filters = ["field_1", ("field_2", "label"), ...]``
    """

    group_column: str = ""
    """An additional column to group the table by. Optional.

    Note that a group column need to be orderable.
    """

    length_options = [(10, "10"), (25, "25"), (50, "50"), (100, "100")]
    """Options for page length to be shown in selector. Optional.

    Set to None to disable the entries widget.
    """

    none_string: str = ""
    """String used to render ``None`` values. Mandatory."""

    order_by: Optional[str] = ""
    """Column name to order by on default. Optional.

    Sort order can be given by a leading ``+`` for ascending or ``-`` for descending.

    Example: ``order_by = "-name"``
    """

    order_columns: Dict[str, str] = {}
    """Field to use for ordering a column instead of it's default (if any).

    Can also be nested field.

    Example: ``order_columns = {"publisher": "publisher__name"}``

    """

    search_fields: List[str] = []
    """Fields to include in full text search.

    The UI search box will only be shown if search fields are defined.
    """

    total_columns: List[str] = []
    """Columns for showing a grand total on the bottom given by their names."""

    totals_string = _("Total")
    """String to be shown in the first column of a totals row."""

    # internal settings - should not be modified by user

    page_kwarg = QueryParam.PAGE

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.ordering:
            raise ImproperlyConfigured(
                "The ordering property is not supported. Please use order_by instead."
            )

        initial_qs = (  # pylint: disable = assignment-from-none
            self.get_initial_queryset()
        )
        if initial_qs is not None:
            self.queryset = initial_qs

        self._columns = self._create_columns()
        self._order_by_index = self._calc_order_by_index()

        if group_column := self._columns.group_column:
            if not group_column.order_field:
                raise ImproperlyConfigured(
                    f"No order field configured for group column: {group_column}"
                )

        if (
            self.paginate_by
            and self.length_options
            and self.paginate_by not in {value for value, _ in self.length_options}
        ):
            raise ImproperlyConfigured(
                f"Paginate not found in length options: {self.paginate_by}"
            )

        if self.total_columns:
            for column_name in self.total_columns:
                if not self._columns.has_column(column_name):
                    raise ImproperlyConfigured(
                        f"Can not show total for unknown column: {column_name}"
                    )

        self._filters_def = self._normalize_filter_def()

    def _create_columns(self) -> Columns:
        """Return columns object created from class configuration."""
        if not self.columns:
            raise ImproperlyConfigured("No columns defined")

        columns = self._create_columns_from_def()
        self._update_order_fields_from_def(columns)
        self._add_formatters_from_def(columns)
        return columns

    def _create_columns_from_def(self) -> Columns:
        total_columns_def = set(self.total_columns)

        all_columns = list(self.columns)
        if self.group_column:
            all_columns.append(self.group_column)

        columns = Columns()
        for index, obj in enumerate(all_columns, start=1):
            if isinstance(obj, tuple):
                name, label = obj
            else:
                name, label = obj, ""

            render_func = getattr(self, name, None)
            if render_func:
                field = None
                if not callable(render_func):
                    raise ImproperlyConfigured(
                        f"Column {name} must be a callable"
                    ) from None

            else:
                field = self._find_field_by_name(name)

            if not field and not render_func:
                raise ImproperlyConfigured(
                    f"Column {name} must be a field or a callable."
                )

            if self.group_column:
                is_group_column = self.group_column == name
            else:
                is_group_column = False

            columns.add(
                Column(
                    name=name,
                    index=index,
                    field=field,
                    label=label,
                    render_func=render_func,
                    is_group_column=is_group_column,
                    is_total_column=name in total_columns_def,
                )
            )

        return columns

    def _update_order_fields_from_def(self, columns: Columns) -> None:
        """Update order field for columns from def."""
        for column_name, order_field in self.order_columns.items():
            try:
                column = columns.by_name(column_name)
            except KeyError:
                raise ImproperlyConfigured(
                    f"Column {column_name} referenced in order_columns does not exist."
                ) from None

            column.order_field = order_field

    def _add_formatters_from_def(self, columns: Columns) -> None:
        """Update column formatter from def."""
        for column_name, formatter_def in self.format_columns.items():
            try:
                column = columns.by_name(column_name)
            except KeyError:
                raise ImproperlyConfigured(
                    f"Column {column_name} referenced in format_columns does not exist."
                ) from None

            if isinstance(formatter_def, tuple):
                formatter = formatter_def[0]
                formatter_param = formatter_def[1]
            else:
                formatter = formatter_def
                formatter_param = ""

            if not isinstance(formatter, ColumnFormatter):
                raise ImproperlyConfigured(f"Invalid column formatter: {formatter_def}")

            column.formatter = formatter
            column.formatter_param = formatter_param

    def _find_field_by_name(self, field_name: str) -> Optional[models.Field]:
        """Return corresponding field when found, else return None."""
        qs = super().get_queryset()
        try:
            return qs.model._meta.get_field(field_name)
        except FieldDoesNotExist:
            return None

    def _calc_order_by_index(self) -> Optional[int]:
        if not self.order_by:
            return None

        sort_order, column_name = self._parse_order_by(self.order_by)
        order_column = self._match_column_for_order_by(column_name)

        return order_column.index * sort_order

    def _match_column_for_order_by(self, column_name: str) -> Column:
        try:
            order_column = self._columns.by_name(column_name)
        except KeyError:
            raise ImproperlyConfigured(
                f"Invalid column for order_by: {self.order_by}"
            ) from None

        if not order_column.order_field:
            raise ValueError(f"No order field defined for: {order_column}")

        if order_column.is_group_column:
            raise ImproperlyConfigured(f"Can not order by group column: {order_column}")

        return order_column

    @staticmethod
    def _parse_order_by(order_by: str) -> Tuple[int, str]:
        if order_by.startswith("-"):
            sort_order = -1
            column_name = order_by[1:]
        elif order_by.startswith("+"):
            sort_order = 1
            column_name = order_by[1:]
        else:
            sort_order = 1
            column_name = order_by
        return sort_order, column_name

    def _normalize_filter_def(self) -> Dict[str, Tuple[str, str]]:
        """Return filter definition normalized."""
        filters_normalized = {}
        for obj in self.filters:
            if isinstance(obj, tuple):
                field_name = obj[0]
                label = obj[1].title()
            else:
                field_name = obj
                label = field_name
            label = label.replace("_", " ").title()
            filters_normalized[field_name] = (field_name, label)
        return filters_normalized

    def _order_by(self) -> Optional[int]:
        """Return current order by index or None."""
        if order := self.request.GET.get(QueryParam.ORDER_BY):
            return int(order)
        return self._order_by_index

    def _search_query(self):
        return self.request.GET.get(QueryParam.SEARCH, "") if self.search_fields else ""

    def _filters_selected(self):
        if not self.filters:
            return {}
        return {
            k[2:]: unquote(v)
            for k, v in self.request.GET.items()
            if k.startswith(QueryParam.FILTER_PREFIX) and v
        }

    def get_initial_queryset(self):
        """Return the initial queryset to use for this view.

        This method must be overwritten for defining complex queries
        instead of `get_queryset()`.
        """
        return None

    def get_data_queryset(self):
        """Returns the base queryset used for querying the data.

        This can be used to add elements to a queryset, which are expensive to run and
        only needed for the data, but not to calculate the filter options.
        """
        return super().get_queryset()

    def get_queryset(self):  # DO NOT OVERWRITE
        qs = self.get_data_queryset()
        if filters_selected := self._filters_selected():
            qs = qs.filter(**filters_selected)
        if search_query := self._search_query():
            query = Q()
            for field in self.search_fields:
                params = {f"{field}__icontains": search_query}
                query |= Q(**params)
            qs = qs.filter(query)

        order_fields = []
        if group_colum := self._columns.group_column:
            order_fields.append(group_colum.order_field)

        if order_by := self._order_by():
            order_column = self._columns.by_index(abs(order_by))
            order_field = order_column.order_field
            sig = "-" if order_by < 0 else ""
            order_fields.append(f"{sig}{order_field}")

        if order_fields:
            try:
                qs = qs.order_by(*order_fields)
            except FieldError:
                field_list = ", ".join(order_fields)
                raise RuntimeError(
                    f"Can not order by these fields: {field_list}"
                ) from None

        return qs

    def get_paginate_by(self, queryset: Optional[models.QuerySet]):
        if paginate_by := self.request.GET.get(QueryParam.PAGINATE_BY):
            return int(paginate_by)

        return super().get_paginate_by(queryset)  # type: ignore

    def _current_subview(self) -> QueryParam.SUBVIEW:
        """Return current subview."""
        subview = _SubView(self.request.GET.get(QueryParam.SUBVIEW, _SubView.DATA))
        return subview

    def get_template_names(self) -> List[str]:
        """Return template needed to render current subview."""
        subview = self._current_subview()
        template_name = f"htmx_datatables/_{subview.value}.html"
        return [template_name]

    def get_context_data(self, **kwargs):
        """Return the context data."""
        context: Dict[str, Any] = {}  # context shared by all subviews, except data
        self._add_common_context(context)

        subview = self._current_subview()
        if subview is _SubView.MAIN:
            context["filters"] = self._filters_def.values()
            context["length_options"] = (
                self.length_options if self.paginate_by else None
            )
            context["search_enabled"] = len(self.search_fields) > 0
            context["search_query"] = self._search_query()
            return context

        if subview is _SubView.FILTER:
            field_name = self._extract_filter_field_name()
            if not self._filters_def:
                raise ValueError("No filters defined")
            if field_name not in self._filters_def:
                raise ValueError(f"No filter defined for {field_name}")

            context["field_name"] = field_name
            context["filter_options"] = self._filter_options(field_name)
            return context

        if subview is _SubView.DATA:  # this is the actual list view
            context = super().get_context_data(**kwargs)
            self._add_common_context(context)

            if page_obj := context["page_obj"]:
                context["page_range"] = page_obj.paginator.get_elided_page_range(
                    page_obj.number, on_each_side=2, on_ends=1
                )
            order_by = self._order_by()
            context["headers"] = self._build_headers_context(order_by)
            context["data"] = self._render_data(context["object_list"])
            context["order_by"] = order_by if order_by else ""
            context["totals"] = self._build_totals_row()

            return context

        raise NotImplementedError(subview)

    def _add_common_context(self, context: dict):
        context["root_id"] = self.html_root_id()
        context["is_dark_mode"] = int(self.request.GET.get(QueryParam.DARK_MODE, 0))
        add_enum_to_context(QueryParam, context)
        add_enum_to_context(ColumnFormatter, context)

    def _extract_filter_field_name(self) -> str:
        """Extract field name for filter view from current GET request and return it.

        Raises ValueError if field name parameter is missing.
        """
        names = [
            k[2:]
            for k in self.request.GET.keys()
            if k.startswith(QueryParam.FILTER_PREFIX)
        ]
        try:
            return names.pop()
        except IndexError:
            raise ValueError(
                "Missing field parameter for filter in GET request"
            ) from None

    def _filter_options(self, field_name: str) -> List[Tuple[str, Any]]:
        """Return generated options for a field."""
        qs = super().get_queryset()
        values = qs.values_list(field_name, flat=True).distinct()

        field = self._find_field_by_name(field_name)
        if field and (related_model := field.related_model):
            objs = related_model.objects.in_bulk(values)
            options = sorted(
                ((id, str(obj)) for id, obj in objs.items()), key=lambda o: o[1]
            )

        elif field and (choices := field.choices):
            choices_map = dict(choices)
            options = sorted(
                ((value, choices_map[value]) for value in values), key=lambda o: o[1]
            )

        else:
            values_sorted = sorted(
                value for value in values if value is not None and value != ""
            )
            values_stringified = map(str, values_sorted)

            if values_sorted and isinstance(values_sorted[0], bool):
                labels_sorted = map(self._yesno_str, values_sorted)
            else:
                labels_sorted = values_sorted

            options = list(zip(values_stringified, labels_sorted))

        label = self._filters_def[field_name][1]
        options = [("", f"({label})")] + options
        return options

    @staticmethod
    def _yesno_str(value: bool) -> str:
        """Convert a boolean into a meaningful string."""
        if value is True:
            return _("yes")
        if value is False:
            return _("no")
        raise NotImplementedError(f"Unexpected value: {value}")

    def _build_headers_context(self, order_by):
        headers = []
        for column in self._columns.exclude_group_column():
            if column.can_sort:
                idx = column.index
                next_idx = idx if order_by != idx else -idx
                asc = order_by == idx
                desc = order_by == -idx
            else:
                next_idx = asc = desc = None

            column = {
                "label": column.label,
                "idx": next_idx,
                "asc": asc,
                "desc": desc,
                "can_sort": column.can_sort,
            }
            headers.append(column)
        return headers

    def _build_totals_row(self) -> list:
        """Return row with calculated totals (if any)."""
        total_columns = list(self._columns.total_columns())
        if not total_columns:
            return []

        first_column = self._columns.by_index(1)
        values = {first_column.name: str(self.totals_string)}

        qs = ListView.get_queryset(self)
        query = [Sum(column.name) for column in total_columns]
        totals_query = qs.aggregate(*query)
        for column in total_columns:
            column_name = column.name
            temp_obj = SimpleNamespace()
            setattr(temp_obj, column_name, totals_query[f"{column_name}__sum"])
            value = self._render_column(temp_obj, column)
            values[column.name] = value

        obj = SimpleNamespace()
        for column in self._columns.exclude_group_column():
            column_name = column.name
            value = values.get(column_name, self.none_string)
            setattr(obj, column_name, value)

        cells = self._render_cells(obj)
        row = DataRow(cells=tuple(cells))
        return row

    def _render_data(self, object_list) -> List[DataRow]:
        """Render all data for output to the template."""
        rows: List[DataRow] = []
        last_group_value = ""
        group_title = ""
        for obj in object_list:
            if group_column := self._columns.group_column:
                group_value = self._render_column(obj, group_column)
                if last_group_value != group_value:
                    last_group_value = group_title = group_value
                else:
                    group_title = ""

            cells = self._render_cells(obj)
            row = DataRow(cells=tuple(cells), group_title=group_title)
            rows.append(row)

        return rows

    def _render_cells(self, obj):
        """Render item into cells and return them."""
        cells = []
        for column in self._columns.exclude_group_column():
            try:
                value = self._render_column(obj, column)
            except (ObjectDoesNotExist, AttributeError):
                value = self.none_string

            if column.formatter:
                formatter = column.formatter.value
                formatter_param = column.formatter_param
            else:
                formatter = ColumnFormatter.UNDEFINED.value
                formatter_param = ""

            cells.append(
                DataCell(
                    value=value, formatter=formatter, formatter_param=formatter_param
                )
            )

        return cells

    def _render_column(self, obj, column: Column) -> Any:
        """Render column to data.

        Extend this method to add custom rendering for columns.

        Args:
            - obj: Current object to be rendered from the queryset
            - column: Name of the field from the object to be rendered

        Returns:
            Value to be rendered in template
        """
        if column.render_func:
            value = column.render_func(obj)
            if isinstance(value, str):
                return conditional_escape(value)
            return value

        field_name = column.name
        if hasattr(obj, f"get_{field_name}_display"):
            value = getattr(obj, f"get_{field_name}_display")()
        else:
            value = getattr(obj, field_name)

        if isinstance(value, models.Model):
            return str(value)

        if isinstance(value, bool):
            return self._yesno_str(value)

        if value is None:
            return self.none_string

        return value

    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @classmethod
    def html_root_id(cls) -> str:
        """Return HTML root ID for this class."""
        class_name = camel_to_snake(cls.__name__).replace("_", "-")
        return f"hdt-{class_name}"
