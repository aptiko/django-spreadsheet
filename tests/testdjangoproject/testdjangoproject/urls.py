from django.urls import path

from testapp import views

urlpatterns = [
    path(
        "downloadbooks/",
        views.DownloadBooksWorkbookView.as_view(),
        name="download-books",
    ),
]
