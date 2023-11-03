"""Models for example app.

These models are based on the example models from the
Django documentation about Aggregations.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.street} - {self.city}"


class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    age = models.IntegerField(null=True, default=None)
    is_married = models.BooleanField(null=True, default=None)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, null=True, related_name="author"
    )

    def __str__(self) -> str:
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=300, db_index=True)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    class Genre(models.TextChoices):
        BIOGRAPHY = "BI", _("Biography")
        FANTASY = "FA", _("Fantasy")
        HISTORY = "HI", _("History")
        MYSTERY = "MY", _("Mystery")
        ROMANCE = "RO", _("Romance")
        SCIENCE_FICTION = "SF", _("Science Fiction")

    name = models.CharField(max_length=300, db_index=True)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField(_("publication date"), db_index=True)
    genre = models.CharField(max_length=2, choices=Genre.choices)

    def __str__(self) -> str:
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=300, db_index=True)
    books = models.ManyToManyField(Book)

    def __str__(self) -> str:
        return self.name
