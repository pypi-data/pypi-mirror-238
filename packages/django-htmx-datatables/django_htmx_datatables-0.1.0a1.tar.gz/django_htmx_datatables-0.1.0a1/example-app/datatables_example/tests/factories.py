import datetime as dt
import random
from typing import Generic, TypeVar

import factory
import factory.fuzzy
from datatables_example.models import Address, Author, Book, Publisher, Store

T = TypeVar("T")

_faker = factory.faker.faker.Faker()


class _BaseMetaFactory(Generic[T], factory.base.FactoryMetaClass):
    def __call__(cls, *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)


class AddressFactory(
    factory.django.DjangoModelFactory, metaclass=_BaseMetaFactory[Address]
):
    class Meta:
        model = Address

    street = factory.Faker("street_address")
    city = factory.Faker("city")


class AuthorFactory(
    factory.django.DjangoModelFactory, metaclass=_BaseMetaFactory[Author]
):
    class Meta:
        model = Author
        django_get_or_create = ("name",)

    address = factory.SubFactory(AddressFactory)
    age = factory.fuzzy.FuzzyInteger(16, 65)
    is_married = False
    name = factory.Faker("last_name")


class PublisherFactory(
    factory.django.DjangoModelFactory, metaclass=_BaseMetaFactory[Publisher]
):
    class Meta:
        model = Publisher
        django_get_or_create = ("name",)

    name = factory.Faker("company")


class BookFactory(factory.django.DjangoModelFactory, metaclass=_BaseMetaFactory[Book]):
    class Meta:
        model = Book
        django_get_or_create = ("name",)

    genre = factory.fuzzy.FuzzyChoice(Book.Genre.values)
    pages = factory.fuzzy.FuzzyInteger(30, 1000)
    price = factory.fuzzy.FuzzyFloat(10, 250)
    rating = factory.fuzzy.FuzzyInteger(1, 5)
    publisher = factory.SubFactory(PublisherFactory)
    pubdate = factory.fuzzy.FuzzyDateTime(
        dt.datetime(1950, 1, 1, tzinfo=dt.timezone.utc)
    )

    @factory.lazy_attribute
    def name(self):
        num_words = random.randint(3, 5)
        result = " ".join(_faker.words(nb=num_words))
        return result.title()


class StoreFactory(
    factory.django.DjangoModelFactory, metaclass=_BaseMetaFactory[Store]
):
    class Meta:
        model = Store
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda o: f"Book store #{o}")
