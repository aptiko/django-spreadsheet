import django_spreadsheet

from .models import Author, Book


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


class AuthorsWorksheet(django_spreadsheet.Worksheet):
    model = Author
    name = "Authors"
    columns = [{"heading": "Name", "value": "name"}]


class DownloadBooksWorkbookView(django_spreadsheet.WorkbookView):
    filename = "books.xlsx"
    worksheets = [
        BooksWorksheet,
        AuthorsWorksheet,
    ]
