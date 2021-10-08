===========
Quick start
===========

Here is an example. This code should go to ``views.py``::

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
        filename = "books.xlsx"
        worksheets = [
            BooksWorksheet,
        ]

The ``DownloadBooksWorkbookView`` (which you must hook to ``urls.py``)
returns a response with a ``books.xlsx`` file for download. That file is
a workbook containing a single worksheet, ``BooksWorksheet``. Its title
is "Books" and it has two columns, "Author" and "Title". For each
``book``, the "Author" is ``book.author.name`` and the title is
``book.title.capitalize()``.
