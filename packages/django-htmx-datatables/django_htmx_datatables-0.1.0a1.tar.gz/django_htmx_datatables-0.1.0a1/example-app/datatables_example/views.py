from django.db.models import Case, Value, When
from django.shortcuts import render

from htmx_datatables import __version__ as htmx_datatables_version
from htmx_datatables.views import ColumnFormatter, HtmxDataTableView

from . import __version__
from .models import Book


def _common_context() -> dict:
    return {
        "example_version": __version__,
        "htmx_datatables_version": htmx_datatables_version,
    }


def index(request):
    return render(request, "datatables_example/index.html", _common_context())


def bootstrap_3(request):
    return render(request, "datatables_example/bootstrap_3.html", _common_context())


def bootstrap_4(request):
    return render(request, "datatables_example/bootstrap_4.html", _common_context())


def bootstrap_5(request):
    return render(request, "datatables_example/bootstrap_5.html", _common_context())


class BookDataTable(HtmxDataTableView):
    columns = [
        "name",
        "pubdate",
        ("pages", "Total pages"),
        "price",
        "genre",
        "_has_five",
    ]
    format_columns = {
        "price": (ColumnFormatter.FLOATFORMAT, "3g"),
        "_has_five": ColumnFormatter.BOOLEAN,
        "pubdate": (ColumnFormatter.DATE, "SHORT_DATE_FORMAT"),
    }
    filters = ["publisher", "genre", "rating", "has_five"]
    search_fields = ["name"]
    group_column = "publisher"
    order_columns = {"publisher": "publisher__name"}
    paginate_by = 10
    order_by = "name"
    total_columns = ["price"]

    def get_initial_queryset(self):
        return Book.objects.select_related("publisher").annotate(
            has_five=Case(When(rating__gte=5, then=Value(True)), default=Value(False))
        )

    def _has_five(self, obj):
        return obj.has_five
