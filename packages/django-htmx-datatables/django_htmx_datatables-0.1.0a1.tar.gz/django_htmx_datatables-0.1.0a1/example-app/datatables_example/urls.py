from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="datatables_example_index"),
    path("bootstrap-3", views.bootstrap_3, name="datatables_example_bs_3"),
    path("bootstrap-4", views.bootstrap_4, name="datatables_example_bs_4"),
    path("bootstrap-5", views.bootstrap_5, name="datatables_example_bs_5"),
    path(
        "users_data_table/",
        views.BookDataTable.as_view(),
        name="example_books_datatable",
    ),
]
