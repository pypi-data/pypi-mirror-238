from unittest.mock import Mock

from django.db import models
from django.test import TestCase

from htmx_datatables.core import Column, Columns


class TestColum(TestCase):
    def test_should_create_without_field(self):
        # when
        obj = Column(name="alpha_one", index=1)
        # then
        self.assertEqual(obj.name, "alpha_one")
        self.assertEqual(obj.index, 1)
        self.assertEqual(obj.order_field, "")
        self.assertFalse(obj.is_field)
        self.assertFalse(obj.can_sort)
        self.assertEqual(obj.label, "Alpha one")
        self.assertFalse(obj.is_group_column)

    def test_should_create_with_field(self):
        # when
        field = Mock(spec=models.Field)
        field.verbose_name = "alpha one verbose"
        obj = Column(name="alpha_one", index=1, field=field)
        # then
        self.assertEqual(obj.field, field)
        self.assertTrue(obj.is_field)
        self.assertEqual(obj.order_field, "alpha_one")
        self.assertTrue(obj.can_sort)
        self.assertEqual(obj.label, "Alpha one verbose")
        self.assertFalse(obj.is_group_column)

    def test_should_fall_back_on_label_when_field_has_no_verbose_name(self):
        # when
        field = Mock(spec=models.Field)
        obj = Column(name="alpha_one", index=1, field=field)
        # then
        self.assertEqual(obj.label, "Alpha one")

    def test_should_set_custom_order_field(self):
        # when
        field = Mock(spec=models.Field)
        obj = Column(name="alpha_one", index=1, field=field, order_field="special")
        # then
        self.assertEqual(obj.order_field, "special")
        self.assertTrue(obj.can_sort)

    def test_should_set_custom_label(self):
        # when
        obj = Column(name="alpha_one", index=1, label="special")
        # then
        self.assertEqual(obj.label, "special")

    def test_should_remove_underscore_from_label_when_function(self):
        # when
        obj = Column(name="_special", index=1, render_func=lambda: None)
        # then
        self.assertEqual(obj.label, "Special")


class TestColumns(TestCase):
    def test_should_create_empty(self):
        # when
        obj = Columns()
        # then
        self.assertIsInstance(obj, Columns)

    def test_should_return_length(self):
        # given
        columns = Columns()
        column = Column(name="abc", index=1)
        # when
        columns.add(column)
        # then
        self.assertEqual(len(columns), 1)

    def test_should_return_by_name(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2)
        columns.add(alpha)
        columns.add(bravo)
        # when
        obj = columns.by_name("bravo")
        # then
        self.assertEqual(obj, bravo)

    def test_should_return_by_index(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2)
        columns.add(alpha)
        columns.add(bravo)
        # when
        obj = columns.by_index(2)
        # then
        self.assertEqual(obj, bravo)

    def test_should_return_true_if_column_exists(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2)
        columns.add(alpha)
        columns.add(bravo)
        # when/then
        self.assertTrue(columns.has_column("bravo"))

    def test_should_return_false_if_column_does_not_exists(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2)
        columns.add(alpha)
        columns.add(bravo)
        # when/then
        self.assertFalse(columns.has_column("charlie"))

    def test_should_return_iterator(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2)
        columns.add(alpha)
        columns.add(bravo)
        # when
        result = list(columns)
        # then
        self.assertEqual(result, [alpha, bravo])

    def test_should_not_allow_adding_column_with_existing_index(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=1)
        columns.add(alpha)
        # when/then
        with self.assertRaises(ValueError):
            columns.add(bravo)

    def test_should_not_allow_adding_column_with_existing_name(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="alpha", index=2)
        columns.add(alpha)
        # when/then
        with self.assertRaises(ValueError):
            columns.add(bravo)

    def test_should_return_clone_without_group_column_1(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2, is_group_column=True)
        charlie = Column(name="charlie", index=3)
        columns.add(alpha)
        columns.add(bravo)
        columns.add(charlie)
        # when
        result = columns.exclude_group_column()
        # then
        self.assertEqual(list(result), [alpha, charlie])

    def test_should_return_clone_without_group_column_2(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2)
        charlie = Column(name="charlie", index=3)
        columns.add(alpha)
        columns.add(bravo)
        columns.add(charlie)
        # when
        result = columns.exclude_group_column()
        # then
        self.assertEqual(list(result), [alpha, bravo, charlie])

    def test_should_return_group_column(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2, is_group_column=True)
        columns.add(alpha)
        columns.add(bravo)
        # when/then
        self.assertEqual(columns.group_column, bravo)

    def test_should_return_none_when_no_group_column_exists(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1)
        bravo = Column(name="bravo", index=2)
        columns.add(alpha)
        columns.add(bravo)
        # when/then
        self.assertIsNone(columns.group_column)

    def test_should_return_total_columns(self):
        # given
        columns = Columns()
        alpha = Column(name="alpha", index=1, is_total_column=False)
        bravo = Column(name="bravo", index=2, is_total_column=True)
        charlie = Column(name="charlie", index=3, is_total_column=True)
        columns.add(alpha)
        columns.add(bravo)
        columns.add(charlie)
        # when
        self.assertEqual(list(columns.total_columns()), [bravo, charlie])
