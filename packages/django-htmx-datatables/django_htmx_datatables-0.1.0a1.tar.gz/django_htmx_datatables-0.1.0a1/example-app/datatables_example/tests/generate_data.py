"""Generate data for load testing.

This script can be executed directly from shell.
"""
# flake8: noqa
import argparse
import os
import sys
from pathlib import Path

# parse command line arguments
parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--max-books", type=int, default=1000, help="Max amount of books generated"
)
parser.add_argument(
    "--max-authors", type=int, default=100, help="Max amount of authors generated"
)
parser.add_argument(
    "--max-publishers",
    type=int,
    default=10,
    help="Max amount of publishers generated",
)
parser.add_argument(
    "--max-stores", type=int, default=20, help="Max amount of stores generated"
)
parser.add_argument(
    "--delete-stale", action="store_true", help="Max amount of stores generated"
)
_path = Path.cwd()
parser.add_argument("--django-path", default=_path, help="Path to django root")
parser.add_argument(
    "--django-settings", default="myauth.settings.local", help="Django settings path"
)
args = parser.parse_args()

sys.path.insert(0, str(args.django_path))

# init and setup django project
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", args.django_settings)
print("Starting Django...")
django.setup()

"""SCRIPT"""
import random

import tqdm
from datatables_example.models import Author, Book, Publisher, Store
from datatables_example.tests.factories import (
    AuthorFactory,
    BookFactory,
    PublisherFactory,
    StoreFactory,
)

if args.delete_stale:
    print("Deleting stale objects...")
    Store.objects.all().delete()
    Book.objects.all().delete()
    Publisher.objects.all().delete()
    Author.objects.all().delete()

print(f"Creating { args.max_publishers} publishes...")
publishers = PublisherFactory.create_batch(args.max_publishers)
print(f"Creating {args.max_stores} stores...")
stores = StoreFactory.create_batch(args.max_stores)

authors = []
for _ in tqdm.tqdm(range(args.max_authors), desc="Creating authors", unit="authors"):
    params = {}
    if random.random() <= 0.2:
        params["address"] = None

    authors.append(AuthorFactory(**params))

for _ in tqdm.tqdm(range(args.max_books), desc="Creating books", unit="book"):
    book = BookFactory(publisher=random.choice(publishers))
    book_authors = random.sample(authors, random.randint(1, 3))
    book.authors.set(book_authors)
