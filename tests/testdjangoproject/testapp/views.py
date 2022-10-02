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

    def get_author_name(self, author):
        return author.name

    columns = [{"heading": "Name", "value": get_author_name}]


class DownloadBooksWorkbookView(django_spreadsheet.WorkbookView):
    filename = "books.xlsx"
    worksheets = [
        BooksWorksheet,
        AuthorsWorksheet,
    ]
