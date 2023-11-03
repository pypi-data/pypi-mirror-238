# django-htmx-datatables example app

This Django app demonstrates the key feature of django-htmx-datatables.

## Installation

Install the app directly from the repo:

```sh
pip install git+https://gitlab.com/ErikKalkoken/django-htmx-datatables.git@master#subdirectory=example-app
```

Then add it to `INSTALLED_APPS` in your settings.

You also need to add the urls of this app to your project's main urls file:

```python
...
urlpatterns = [
    ...
    path("datatables_example/", include("datatables_example.urls")),
    ...
]

```

Then run migrations & collectstatic.

Finally, restart your Django server.

The app should now be live at: `www.your-server.com/datatables_example/`

## Generate data

To see any data you need to generate it. You can do this with the following command:

```sh
python -m datatables_example.tests.generate_data
```

Note that the command is designed to be run from your Django project's main folder, the same where you also find `manage.py`.

You can configure how many objects you want to generate and Django specifics via parameters:

```text
usage: generate_data.py [-h] [--max-books MAX_BOOKS] [--max-authors MAX_AUTHORS]
                        [--max-publishers MAX_PUBLISHERS] [--max-stores MAX_STORES] [--delete-stale]
                        [--django-path DJANGO_PATH] [--django-settings DJANGO_SETTINGS]

Generate data for load testing. This script can be executed directly from shell.

options:
  -h, --help            show this help message and exit
  --max-books MAX_BOOKS
                        Max amount of books generated (default: 1000)
  --max-authors MAX_AUTHORS
                        Max amount of authors generated (default: 100)
  --max-publishers MAX_PUBLISHERS
                        Max amount of publishers generated (default: 10)
  --max-stores MAX_STORES
                        Max amount of stores generated (default: 20)
  --delete-stale        Max amount of stores generated (default: False)
  --django-path DJANGO_PATH
                        Path to django root (default: /home/erik997/python/projects/aa-dev/django-htmx-
                        datatables)
  --django-settings DJANGO_SETTINGS
                        Django settings path (default: myauth.settings.local)
```
