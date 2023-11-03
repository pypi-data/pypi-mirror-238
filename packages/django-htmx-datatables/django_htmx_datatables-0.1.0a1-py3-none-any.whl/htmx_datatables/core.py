"""Core logic for htmx datatables."""

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from enum import Enum
from typing import Any, Callable, Dict, Generator, List, NamedTuple, Optional, Tuple

from django.db import models


class ColumnFormatter(Enum):
    """A formatter for columns."""

    UNDEFINED = 0
    FLOATFORMAT = 1  # floatformat template filter
    BOOLEAN = 2
    DATE = 3  # date template filter
    YESNO = 4  # yesno template filter


class DataCell(NamedTuple):
    """A data cell."""

    value: Any
    formatter: int = ColumnFormatter.UNDEFINED.value  # must use enum value in template
    formatter_param: str = ""


class DataRow(NamedTuple):
    """A data row of a HtmxDataTableView."""

    cells: Tuple[DataCell, ...]
    group_title: str = ""


@dataclass
class Column:
    """A column in a HtmxDataTableView"""

    name: str
    index: int  # index starts at 1
    field: Optional[models.Field] = None
    order_field: str = ""
    label: str = ""
    is_group_column: bool = False
    is_total_column: bool = False
    render_func: Callable = None
    formatter: Optional[ColumnFormatter] = None
    formatter_param: str = ""

    def __post_init__(self):
        if not self.order_field:
            self.order_field = self.name if self.is_field else ""

        if not self.label:
            if self.is_field:
                try:
                    name = self.field.verbose_name
                except AttributeError:
                    name = self.name
            elif self.render_func:
                name = self.name.removeprefix("_")
            else:
                name = self.name

            self.label = name.replace("_", " ").capitalize()

    def __str__(self) -> str:
        return self.name

    @property
    def is_field(self) -> bool:
        """Return True if column is a Django model field, else False."""
        return self.field is not None

    @property
    def can_sort(self) -> bool:
        """Return True if column is sortable, else False."""
        return bool(self.order_field)


@dataclass
class Columns:
    """Columns in a HtmxDataTableView"""

    _columns: Dict[str, Column] = dataclass_field(default_factory=dict)
    _index_map: Dict[int, str] = dataclass_field(default_factory=dict)
    _group_column: Optional[Column] = None
    _total_columns: List[Column] = dataclass_field(default_factory=list)

    def __iter__(self):
        return iter(sorted(self._columns.values(), key=lambda o: o.index))

    def __len__(self):
        return len(self._columns)

    def add(self, column: Column):
        """Add given column."""
        if column.index in self._index_map:
            raise ValueError(
                f"{column}: Column with index {column.index} already exists"
            )

        if column.name in self._columns:
            raise ValueError(f"{column}: Column with same name already exists")

        self._columns[column.name] = column
        self._index_map[column.index] = column.name

        if column.is_group_column:
            self._group_column = column

    @property
    def group_column(self) -> Optional[Column]:
        """Return group column, when it exists. Otherwise return None."""
        return self._group_column

    def total_columns(self) -> Generator[Column, None, None]:
        """Return sequence of total columns (if any)."""
        return (column for column in self if column.is_total_column)

    def by_name(self, name: str) -> Column:
        """Return a column by name. Raises `KeyError` if not found."""
        return self._columns[name]

    def by_index(self, index: int) -> Column:
        """Return a column by index. Raises `KeyError` if not found."""
        return self._columns[self._index_map[index]]

    def has_column(self, name: str) -> bool:
        """Return True if column with that name exists, else False."""
        return name in self._columns

    def exclude_group_column(self) -> Generator[Column, None, None]:
        """Return columns excluding a potential group column."""
        return (column for column in self if not column.is_group_column)
