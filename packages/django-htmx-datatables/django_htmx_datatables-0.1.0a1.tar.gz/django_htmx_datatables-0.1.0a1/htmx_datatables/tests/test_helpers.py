from enum import Enum

from django.test import TestCase

from htmx_datatables.helpers import add_enum_to_context, camel_to_snake


class TestCameToSnake(TestCase):
    def test_single_word(self):
        self.assertEqual(camel_to_snake("Test"), "test")

    def test_multi_word(self):
        self.assertEqual(camel_to_snake("TestAlpha"), "test_alpha")

    def test_multi_word_and_delimiter(self):
        self.assertEqual(camel_to_snake("TestAlphaBravo", "-"), "test-alpha-bravo")


class TestAddEnumToContext(TestCase):
    def test_should_add_enum_to_context_with_string(self):
        # given
        class MyEnum(Enum):
            ALPHA = "alpha"
            BRAVO = "bravo"

        context = {"other": "stuff"}
        # when
        add_enum_to_context(MyEnum, context)
        # then
        expected = {"ALPHA": "alpha", "BRAVO": "bravo"}
        self.assertDictEqual(context["MyEnum"], expected)

    def test_should_add_enum_to_context_with_int(self):
        # given
        class MyEnum(Enum):
            ALPHA = 1
            BRAVO = 2

        context = {"other": "stuff"}
        # when
        add_enum_to_context(MyEnum, context)
        # then
        expected = {"ALPHA": 1, "BRAVO": 2}
        self.assertDictEqual(context["MyEnum"], expected)
