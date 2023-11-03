from decimal import Decimal

from datatables_example.models import Address, Author, Book
from datatables_example.tests.factories import (
    AddressFactory,
    AuthorFactory,
    BookFactory,
    PublisherFactory,
)
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Value
from django.test import RequestFactory, TestCase
from django.utils.safestring import mark_safe

from htmx_datatables.core import ColumnFormatter, DataCell, DataRow
from htmx_datatables.views import HtmxDataTableView


def data_values(data):
    """Extract values from data for easier testing."""
    result = []
    for row in data:
        result.append([column.value for column in row.cells])
    return result


class TestCaseDataTable(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.factory = RequestFactory()


class TestHeader(TestCaseDataTable):
    def test_should_render_labels_from_field_names(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        labels = [o["label"] for o in response.context_data["headers"]]
        self.assertListEqual(labels, ["Name", "Age"])

    def test_should_render_with_custom_label(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", ("age", "my age")]

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        labels = [o["label"] for o in response.context_data["headers"]]
        self.assertListEqual(labels, ["Name", "my age"])

    def test_should_use_verbose_name_as_label(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["pubdate"]

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        labels = [o["label"] for o in response.context_data["headers"]]
        self.assertListEqual(labels, ["Publication date"])


class TestData(TestCaseDataTable):
    def test_should_render_data_for_two_columns_and_basic_context(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]
            order_by = "name"

        AuthorFactory(name="Peter Parker", age=22)
        AuthorFactory(name="Clark Kent", age=43)
        AuthorFactory(name="Bruce Wayne", age=35)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertIn("htmx_datatables/_data.html", response.template_name)
        context = response.context_data
        self.assertListEqual(
            context["data"],
            [
                DataRow((DataCell("Bruce Wayne"), DataCell(35))),
                DataRow((DataCell("Clark Kent"), DataCell(43))),
                DataRow((DataCell("Peter Parker"), DataCell(22))),
            ],
        )
        self.assertEqual(context["root_id"], "hdt-my-data-table-view")

    def test_should_render_booleans_as_words(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            queryset = Author.objects.order_by("name")
            columns = ["name", "is_married"]

        AuthorFactory(name="alpha", is_married=False)
        AuthorFactory(name="bravo", is_married=True)
        AuthorFactory(name="charlie", is_married=None)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[1].value for obj in response.context_data["data"]]
        self.assertListEqual(data, ["no", "yes", ""])

    def test_should_render_choices_as_labels(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["genre"]

        BookFactory(genre=Book.Genre.FANTASY)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]
        self.assertListEqual(data, ["Fantasy"])

    def test_should_render_foreign_keys_as_str(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["publisher"]

        publisher = PublisherFactory(name="Alpha")
        BookFactory(publisher=publisher)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]
        self.assertListEqual(data, ["Alpha"])

    def test_should_render_missing_related_object_as_none(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Address
            columns = ["city", "author"]
            order_by = "city"

        address_1 = AddressFactory(city="Alpha")
        AddressFactory(city="Bravo")
        AuthorFactory(name="Johnny", address=address_1)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[1].value for obj in response.context_data["data"]]
        self.assertListEqual(data, ["Johnny", ""])

    def test_should_use_initial_queryset_when_specified(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            columns = ["name"]

            def get_initial_queryset(self):
                return Author.objects.filter(age__lt=30)

        AuthorFactory(name="Bruce Wayne", age=35)
        AuthorFactory(name="Peter Parker", age=20)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]
        self.assertListEqual(data, ["Peter Parker"])

    def test_should_detect_field_names_for_ordering(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age", "custom"]

            def custom(self, obj):
                return "dummy"

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [
            {"label": "Name", "idx": 1, "asc": False, "desc": False, "can_sort": True},
            {"label": "Age", "idx": 2, "asc": False, "desc": False, "can_sort": True},
            {
                "label": "Custom",
                "idx": None,
                "asc": None,
                "desc": None,
                "can_sort": False,
            },
        ]
        self.assertListEqual(response.context_data["headers"], expected)


class TestConfigurationErrors(TestCaseDataTable):
    def test_should_raise_error_when_no_columns_defined(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_ordering_defined(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            ordering = "name"

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_order_by_invalid_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            order_by = "invalid"

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_paginate_by_does_not_match_length_options(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            length_options = [(10, "10"), (25, "25")]
            paginate_by = 7

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_colum_neither_field_nor_callable(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["undefined"]

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_group_column_has_no_order_field(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["name"]
            group_column = "age"
            order_columns = {"age": ""}

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_no_order_field_defined_for_group_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            group_column = "my_group"

            def my_group(self, obj):
                return ""

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_attribute_for_a_column_is_not_callable(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            group_column = "my_group"
            my_group = "hello"

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_order_column_reference_is_invalid(
        self,
    ):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            order_columns = {"invalid": "special"}

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_raise_error_when_total_column_is_unknown(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]
            total_columns = ["unknown"]

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_trying_to_order_by_group_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["name"]
            group_column = "rating"
            order_by = "rating"

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_format_column_reference_is_invalid(
        self,
    ):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            format_columns = {"invalid": ColumnFormatter.BOOLEAN}

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)

    def test_should_raise_error_when_formatter_is_invalid(
        self,
    ):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            format_columns = {"name": "invalid"}

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ImproperlyConfigured):
            my_view(request)


class TestCustomColumns(TestCaseDataTable):
    def test_should_render_with_custom_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "special"]
            order_by = "name"

            def special(self, obj):
                return "my-value"

        AuthorFactory(name="Bruce Wayne")
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[1].value for obj in response.context_data["data"]]
        self.assertListEqual(data, ["my-value"])
        expected = [
            {"label": "Name", "idx": -1, "asc": True, "desc": False, "can_sort": True},
            {
                "label": "Special",
                "idx": None,
                "asc": None,
                "desc": None,
                "can_sort": False,
            },
        ]
        self.assertListEqual(response.context_data["headers"], expected)

    def test_should_ignore_underscore_for_column_label(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "_special"]
            order_by = "name"

            def _special(self, obj):
                ...

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        labels = [o["label"] for o in response.context_data["headers"]]
        self.assertListEqual(labels, ["Name", "Special"])

    def test_should_render_with_custom_column_and_order(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "special"]
            order_columns = {"name": "", "special": "age"}
            order_by = "special"

            def special(self, obj):
                return "my-value"

        AuthorFactory(name="Bruce Wayne", age=35)
        AuthorFactory(name="Peter Parker", age=20)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [["Peter Parker", "my-value"], ["Bruce Wayne", "my-value"]]
        self.assertListEqual(data_values(response.context_data["data"]), expected)
        expected = [
            {
                "label": "Name",
                "idx": None,
                "asc": None,
                "desc": None,
                "can_sort": False,
            },
            {
                "label": "Special",
                "idx": -2,
                "asc": True,
                "desc": False,
                "can_sort": True,
            },
        ]
        self.assertListEqual(response.context_data["headers"], expected)

    def test_should_raise_error_when_trying_to_order_by_custom_column_with_default(
        self,
    ):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "special"]
            order_by = "special"

            def special(self, obj):
                return "my-value"

        AuthorFactory()
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ValueError):
            my_view(request)

    def test_should_render_custom_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["special"]

            def special(self, obj):
                return "hello"

        AuthorFactory()
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]

        self.assertEqual(data, ["hello"])

    def test_should_escape_custom_columns(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["special"]

            def special(self, obj):
                return "<span>hello</span>"

        AuthorFactory()
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]

        self.assertEqual(data, ["&lt;span&gt;hello&lt;/span&gt;"])

    def test_should_not_escape_custom_columns_when_marked_safe(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["special"]

            def special(self, obj):
                return mark_safe("<span>hello</span>")

        AuthorFactory()
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]

        self.assertEqual(data, ["<span>hello</span>"])

    def test_should_not_escape_custom_columns_when_not_string(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["special"]

            def special(self, obj):
                return 42

        AuthorFactory()
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]

        self.assertEqual(data, [42])


class TestDarkMode(TestCaseDataTable):
    def test_should_include_enabled_dark_mode(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["name"]

        for subview in ["main", "filter", "data"]:
            with self.subTest(subview=subview):
                request = self.factory.get(f"/?v={subview}&dm=1&f_name=")
                my_view = MyDataTableView.as_view()
                # when
                response = my_view(request)
                # then
                self.assertEqual(response.context_data["is_dark_mode"], 1)

    def test_should_include_disabled_dark_mode(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["name"]

        for subview in ["main", "filter", "data"]:
            with self.subTest(subview=subview):
                request = self.factory.get(f"/?v={subview}&dm=0&f_name=")
                my_view = MyDataTableView.as_view()
                # when
                response = my_view(request)
                # then
                self.assertEqual(response.context_data["is_dark_mode"], 0)

    def test_should_include_default_dark_mode(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["name"]

        for subview in ["main", "filter", "data"]:
            with self.subTest(subview=subview):
                request = self.factory.get(f"/?v={subview}&f_name=")
                my_view = MyDataTableView.as_view()
                # when
                response = my_view(request)
                # then
                self.assertEqual(response.context_data["is_dark_mode"], 0)


class TestFilters(TestCaseDataTable):
    def test_should_render_filter(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["name"]

        request = self.factory.get("/?v=main")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [("name", "Name")]
        self.assertEqual(list(response.context_data["filters"]), expected)

    def test_should_render_filter_with_custom_title(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = [("name", "special")]

        request = self.factory.get("/?v=main")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [("name", "Special")]
        self.assertEqual(list(response.context_data["filters"]), expected)

    def test_should_apply_filter(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["name"]

        AuthorFactory(name="Bruce Wayne")
        AuthorFactory(name="Peter Parker")
        request = self.factory.get("/?f_name=Bruce+Wayne")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [["Bruce Wayne"]]
        self.assertListEqual(data_values(response.context_data["data"]), expected)


class TestFilter(TestCaseDataTable):
    def test_should_render_filter(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["name"]

        AuthorFactory(name="Peter Parker")
        AuthorFactory(name="Clark Kent")
        AuthorFactory(name="")
        request = self.factory.get("/?v=filter&f_name=")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertEqual(response.context_data["field_name"], "name")
        expected = [
            ("", "(Name)"),
            ("Clark Kent", "Clark Kent"),
            ("Peter Parker", "Peter Parker"),
        ]
        self.assertEqual(response.context_data["filter_options"], expected)

    def test_should_render_filter_with_custom_title(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = [("name", "special")]

        AuthorFactory(name="Bruce Wayne")
        request = self.factory.get("/?v=filter&f_name=")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [("", "(Special)"), ("Bruce Wayne", "Bruce Wayne")]
        self.assertEqual(response.context_data["filter_options"], expected)

    def test_should_render_filter_for_booleans(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["is_married"]

        AuthorFactory(is_married=False)
        AuthorFactory(is_married=True)
        AuthorFactory(is_married=True)
        request = self.factory.get("/?v=filter&f_is_married=")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [("", "(Is Married)"), ("False", "no"), ("True", "yes")]
        self.assertEqual(response.context_data["filter_options"], expected)

    def test_should_raise_error_when_field_name_is_missing(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["is_married"]

        request = self.factory.get("/?v=filter")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ValueError):
            my_view(request)

    def test_should_raise_error_when_field_name_is_unknown(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["is_married"]

        request = self.factory.get("/?v=filter&f_unknown=")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ValueError):
            my_view(request)

    def test_should_raise_error_when_no_filters_defined(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]

        request = self.factory.get("/?v=filter&f_unknown=")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ValueError):
            my_view(request)

    def test_should_render_filter_for_custom_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            queryset = Author.objects.annotate(special=Value("dummy"))
            columns = ["name"]
            filters = ["special"]

        AuthorFactory(name="Bruce Wayne")
        request = self.factory.get("/?v=filter&f_special=")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [("", "(Special)"), ("dummy", "dummy")]
        self.assertEqual(response.context_data["filter_options"], expected)

    def test_should_render_filter_for_foreign_key(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["name"]
            filters = ["publisher"]

        PublisherFactory(name="Alpha")
        pub_2 = PublisherFactory(name="Bravo")
        BookFactory(publisher=pub_2)

        request = self.factory.get("/?v=filter&f_publisher=")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertEqual(response.context_data["field_name"], "publisher")
        expected = [("", "(Publisher)"), (pub_2.id, "Bravo")]
        self.assertEqual(response.context_data["filter_options"], expected)

    def test_should_render_filter_for_choices(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["name"]
            filters = ["genre"]

        BookFactory(genre=Book.Genre.FANTASY)
        request = self.factory.get("/?v=filter&f_genre")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertEqual(response.context_data["field_name"], "genre")
        expected = [("", "(Genre)"), ("FA", "Fantasy")]
        self.assertEqual(response.context_data["filter_options"], expected)


class TestFormatColumns(TestCaseDataTable):
    def test_should_add_floatformat_formatter_to_cells(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["price"]
            format_columns = {"price": (ColumnFormatter.FLOATFORMAT, "4g")}

        BookFactory(price=42.34)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [
            DataRow(
                (
                    DataCell(
                        Decimal("42.34"),
                        formatter=ColumnFormatter.FLOATFORMAT.value,
                        formatter_param="4g",
                    ),
                )
            )
        ]
        self.assertListEqual(response.context_data["data"], expected)

    def test_should_add_boolean_formatter_to_cells(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["has_five"]
            format_columns = {"has_five": ColumnFormatter.BOOLEAN}

            def has_five(self, obj):
                return True if obj.rating == 5 else False

        BookFactory(rating=5)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [DataRow((DataCell(True, formatter=ColumnFormatter.BOOLEAN.value),))]
        self.assertListEqual(response.context_data["data"], expected)


class TestNoneValues(TestCaseDataTable):
    def test_should_render_none_values_by_default(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]

        AuthorFactory(name="Bruce Wayne", age=None)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [["Bruce Wayne", ""]]
        self.assertListEqual(data_values(response.context_data["data"]), expected)

    def test_should_render_none_values_with_custom_value(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]
            none_string = "-"

        AuthorFactory(name="Bruce Wayne", age=None)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [["Bruce Wayne", "-"]]
        self.assertListEqual(data_values(response.context_data["data"]), expected)


class TestOrderBy(TestCaseDataTable):
    def test_should_order_by_name_ascending(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]
            order_by = "name"

        AuthorFactory(name="Peter Parker", age=22)
        AuthorFactory(name="Bruce Wayne", age=35)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertIn("htmx_datatables/_data.html", response.template_name)
        expected = [["Bruce Wayne", 35], ["Peter Parker", 22]]
        self.assertListEqual(data_values(response.context_data["data"]), expected)
        expected = [
            {"label": "Name", "idx": -1, "asc": True, "desc": False, "can_sort": True},
            {"label": "Age", "idx": 2, "asc": False, "desc": False, "can_sort": True},
        ]
        self.assertListEqual(response.context_data["headers"], expected)
        self.assertEqual(response.context_data["order_by"], 1)

    def test_should_order_by_first_column_descending(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]
            order_by = "-name"

        AuthorFactory(name="Peter Parker", age=22)
        AuthorFactory(name="Bruce Wayne", age=35)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertIn("htmx_datatables/_data.html", response.template_name)
        expected = [
            ["Peter Parker", 22],
            ["Bruce Wayne", 35],
        ]
        self.assertListEqual(data_values(response.context_data["data"]), expected)
        expected = [
            {"label": "Name", "idx": 1, "asc": False, "desc": True, "can_sort": True},
            {"label": "Age", "idx": 2, "asc": False, "desc": False, "can_sort": True},
        ]
        self.assertListEqual(response.context_data["headers"], expected)
        self.assertEqual(response.context_data["order_by"], -1)

    def test_should_order_by_name_ascending_2(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]
            order_by = "+name"

        AuthorFactory(name="Peter Parker", age=22)
        AuthorFactory(name="Bruce Wayne", age=35)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [
            ["Bruce Wayne", 35],
            ["Peter Parker", 22],
        ]
        self.assertListEqual(data_values(response.context_data["data"]), expected)
        self.assertEqual(response.context_data["order_by"], 1)

    def test_should_order_by_second_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]
            order_by = "age"

        AuthorFactory(name="Peter Parker", age=22)
        AuthorFactory(name="Clark Kent", age=44)
        AuthorFactory(name="Bruce Wayne", age=35)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [
            ["Peter Parker", 22],
            ["Bruce Wayne", 35],
            ["Clark Kent", 44],
        ]
        self.assertListEqual(data_values(response.context_data["data"]), expected)
        expected = [
            {"label": "Name", "idx": 1, "asc": False, "desc": False, "can_sort": True},
            {"label": "Age", "idx": -2, "asc": True, "desc": False, "can_sort": True},
        ]
        self.assertListEqual(response.context_data["headers"], expected)
        self.assertEqual(response.context_data["order_by"], 2)

    def test_should_order_by_first_column_from_param(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name", "age"]
            order_by = "age"

        AuthorFactory(name="Peter Parker", age=22)
        AuthorFactory(name="Clark Kent", age=44)
        request = self.factory.get("/?o=1")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [
            ["Clark Kent", 44],
            ["Peter Parker", 22],
        ]
        self.assertListEqual(data_values(response.context_data["data"]), expected)


class TestOrderColumns(TestCaseDataTable):
    def test_should_use_field_name_for_ordering_by_default(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["publisher"]
            order_by = "publisher"

        pub_2 = PublisherFactory(name="Bravo")
        pub_1 = PublisherFactory(name="Alpha")
        BookFactory(publisher=pub_2)
        BookFactory(publisher=pub_1)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]
        self.assertListEqual(data, ["Bravo", "Alpha"])

    def test_should_use_order_column_for_ordering(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["publisher"]
            order_columns = {"publisher": "publisher__name"}
            order_by = "publisher"

        pub_2 = PublisherFactory(name="Bravo")
        pub_1 = PublisherFactory(name="Alpha")
        BookFactory(publisher=pub_2)
        BookFactory(publisher=pub_1)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        data = [obj.cells[0].value for obj in response.context_data["data"]]
        self.assertListEqual(data, ["Alpha", "Bravo"])

    def test_should_raise_error_when_trying_to_order_by_disabled_order_column(
        self,
    ):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            order_columns = {"name": ""}
            order_by = "name"

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ValueError):
            my_view(request)

    def test_should_raise_error_when_an_order_field_is_invalid(
        self,
    ):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            order_columns = {"name": "special"}
            order_by = "name"

        AddressFactory()
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(RuntimeError):
            my_view(request)


class TestPaginate(TestCaseDataTable):
    def test_should_use_paginate_from_class(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            paginate_by = 10
            order_by = "name"

        AuthorFactory.create_batch(20)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        page_obj = response.context_data["page_obj"]
        self.assertEqual(page_obj.end_index(), 10)

    def test_should_use_paginate_from_query(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            paginate_by = 10
            order_by = "name"

        AuthorFactory.create_batch(30)
        request = self.factory.get("/?n=20")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        page_obj = response.context_data["page_obj"]
        self.assertEqual(page_obj.end_index(), 20)

    def test_should_disable_pagination(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]

        AuthorFactory.create_batch(20)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertIsNone(response.context_data["page_obj"])


class TestSearch(TestCaseDataTable):
    def test_should_enable_search_when_defined(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            search_fields = ["name"]

        request = self.factory.get("/?v=main")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertTrue(response.context_data["search_enabled"])

    def test_should_apply_search(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            search_fields = ["name"]

        AuthorFactory(name="Bruce Wayne")
        AuthorFactory(name="Peter Parker")
        request = self.factory.get("/?q=Bruce+Wayne")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [["Bruce Wayne"]]
        self.assertListEqual(data_values(response.context_data["data"]), expected)


class TestSubViews(TestCaseDataTable):
    def test_should_render_main_subview(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]

        request = self.factory.get("/?v=main")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertEqual(response.template_name[0], "htmx_datatables/_main.html")

    def test_should_render_filter_subview(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]
            filters = ["name"]

        request = self.factory.get("/?v=filter&f_name=")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertEqual(response.template_name[0], "htmx_datatables/_filter.html")

    def test_should_render_data_subview(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]

        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        self.assertEqual(response.template_name[0], "htmx_datatables/_data.html")

    def test_should_raise_error_when_subview_is_invalid(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Author
            columns = ["name"]

        request = self.factory.get("/?v=invalid")
        my_view = MyDataTableView.as_view()
        # when/then
        with self.assertRaises(ValueError):
            my_view(request)


class TestTotals(TestCaseDataTable):
    def test_should_render_total_one_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["name", "pubdate", "pages"]
            total_columns = ["pages"]

        BookFactory(pages=2)
        BookFactory(pages=3)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = DataRow((DataCell("Total"), DataCell(""), DataCell(5)))
        self.assertEqual(response.context_data["totals"], expected)

    def test_should_render_total_two_columns(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            queryset = Author.objects.annotate(dummy=Value(3))
            columns = ["name", "age", "dummy"]
            total_columns = ["age", "dummy"]

            def dummy(self, obj):
                return obj.dummy

        AuthorFactory(name="Bruce Wayne", age=35)
        AuthorFactory(name="Peter Parker", age=22)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = DataRow((DataCell("Total"), DataCell(57), DataCell(6)))
        self.assertEqual(response.context_data["totals"], expected)

    # def test_should_render_total_with_custom_column_render(self):
    #     # given
    #     class MyDataTableView(HtmxDataTableView):
    #         model = Author
    #         columns = ["name", "age"]
    #         total_columns = ["age"]

    #         def render_column(self, obj, column):
    #             value = super().render_column(obj, column)
    #             if column.name == "age":
    #                 value = f"{value:.2f}"
    #             return value

    #     AuthorFactory(name="Bruce Wayne", age=35)
    #     AuthorFactory(name="Peter Parker", age=22)
    #     request = self.factory.get("/")
    #     my_view = MyDataTableView.as_view()
    #     # when
    #     response = my_view(request)
    #     # then
    #     self.assertListEqual(response.context_data["totals"], ["Total", "57.00"])


class TestGrouping(TestCaseDataTable):
    def test_should_render_data_for_two_columns_with_group_title(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["name", "pages"]
            group_column = "rating"

        BookFactory(name="Charlie", rating=2, pages=100)
        BookFactory(name="Alpha", rating=1, pages=200)
        BookFactory(name="Bravo", rating=1, pages=300)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [
            DataRow((DataCell("Alpha"), DataCell(200)), group_title=1),
            DataRow((DataCell("Bravo"), DataCell(300))),
            DataRow((DataCell("Charlie"), DataCell(100)), group_title=2),
        ]
        self.assertEqual(response.context_data["data"], expected)
        expected = [
            {"label": "Name", "idx": 1, "asc": False, "desc": False, "can_sort": True},
            {"label": "Pages", "idx": 2, "asc": False, "desc": False, "can_sort": True},
        ]
        self.assertListEqual(response.context_data["headers"], expected)

    def test_should_group_by_custom_column(self):
        # given
        class MyDataTableView(HtmxDataTableView):
            model = Book
            columns = ["name"]
            group_column = "special"
            order_columns = {"special": "rating"}
            order_by = "name"

            def special(self, obj):
                return f"Special: {obj.rating}"

        BookFactory(name="Charlie", rating=2)
        BookFactory(name="Bravo", rating=1)
        BookFactory(name="Alpha", rating=1)
        request = self.factory.get("/")
        my_view = MyDataTableView.as_view()
        # when
        response = my_view(request)
        # then
        expected = [
            DataRow((DataCell("Alpha"),), group_title="Special: 1.0"),
            DataRow((DataCell("Bravo"),)),
            DataRow((DataCell("Charlie"),), group_title="Special: 2.0"),
        ]
        self.assertListEqual(response.context_data["data"], expected)
