from functools import partial

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

    @staticmethod
    def get_author_attr(attrname, self, author):
        """This is another way of doing the same thing as get_author_name,
        but using "partial"; it is intended to check that passing partial
        functions also works (because it once didn't).
        """
        return getattr(author, attrname)

    columns = [
        {"heading": "Name", "value": get_author_name},
        {"heading": "Name2", "value": partial(get_author_attr, "name")},
    ]


class DownloadBooksWorkbookView(django_spreadsheet.WorkbookView):
    filename = "books.xlsx"
    worksheets = [
        BooksWorksheet,
        AuthorsWorksheet,
    ]
