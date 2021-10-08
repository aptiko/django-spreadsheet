import django_spreadsheet

from .models import Book


class BooksWorksheet(django_spreadsheet.Worksheet):
    model = Book
    name = "Books"
    columns = [
        {
            "heading": "Author",
            "value": "author.name",
        },
        {
            "heading": "Title",
            "value": lambda book: book.title.capitalize(),
        },
    ]


class DownloadBooksWorkbookView(django_spreadsheet.WorkbookView):
    filename = "bookx.xlsx"
    worksheets = [
        BooksWorksheet,
    ]
