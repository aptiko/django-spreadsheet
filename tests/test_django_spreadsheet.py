from io import BytesIO

from django.test import RequestFactory, SimpleTestCase, TestCase

import openpyxl

from django_spreadsheet import Workbook, WorkbookView, Worksheet
from testapp.models import Author, Book
from testapp.views import BooksWorksheet


class WorkbookViewTestCase(TestCase):
    def setUp(self):
        self.response = self.client.get("/downloadbooks/")

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_filename(self):
        self.assertEqual(
            self.response["Content-Disposition"],
            "attachment; filename=books.xlsx",
        )

    def test_mimetype(self):
        self.assertEqual(
            self.response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def test_returned_workbook_contains_two_sheets(self):
        wb = openpyxl.load_workbook(BytesIO(self.response.content))
        self.assertEqual(wb.sheetnames, ["Books", "Authors"])


class GetWorksheetBodyMixin:
    def _get_body(self, worksheet_name):
        worksheet = self.wb[worksheet_name]
        result = []
        first = True
        for row in worksheet.rows:
            if first:
                first = False
                continue
            result.append([cell.value for cell in row])
        return result


class WorksheetTestCase(TestCase, GetWorksheetBodyMixin):
    @classmethod
    def setUpTestData(cls):
        tolkien = Author.objects.create(name="J.R.R.Tolkien")
        rowling = Author.objects.create(name="J.K.Rowling")
        Book.objects.create(author=tolkien, title="The Hobbit")
        Book.objects.create(author=tolkien, title="The Lord of the Rings")
        Book.objects.create(author=rowling, title="The Prisoner of Azkaban")
        Book.objects.create(author=rowling, title="The Goblet of Fire")

    def setUp(self):
        self.response = self.client.get("/downloadbooks/")
        self.wb = openpyxl.load_workbook(BytesIO(self.response.content))

    def test_headings_in_authors(self):
        first_row = next(self.wb["Authors"].rows)
        self.assertEqual([cell.value for cell in first_row], ["Name", "Name2"])

    def test_headings_in_books(self):
        first_row = next(self.wb["Books"].rows)
        self.assertEqual([cell.value for cell in first_row], ["Author", "Title"])

    def test_body_in_authors(self):
        body = self._get_body("Authors")
        self.assertEqual(
            body,
            [["J.K.Rowling", "J.K.Rowling"], ["J.R.R.Tolkien", "J.R.R.Tolkien"]],
        )

    def test_body_in_books(self):
        body = self._get_body("Books")
        self.assertEqual(
            body,
            [
                ["J.K.Rowling", "The goblet of fire"],
                ["J.K.Rowling", "The prisoner of azkaban"],
                ["J.R.R.Tolkien", "The hobbit"],
                ["J.R.R.Tolkien", "The lord of the rings"],
            ],
        )

    def test_heading_is_bold(self):
        self.assertTrue(self.wb["Books"].row_dimensions[1].font.bold)

    def test_body_is_not_bold(self):
        self.assertFalse(self.wb["Books"].row_dimensions[2].font.bold)

    def test_column_width(self):
        self.assertAlmostEqual(
            self.wb["Books"].column_dimensions["B"].width,
            len("The prisoner of azkaban") * 1.23,
        )


class GetQuerysetTestCase(TestCase, GetWorksheetBodyMixin):
    @classmethod
    def setUpTestData(cls):
        tolkien = Author.objects.create(name="J.R.R.Tolkien")
        rowling = Author.objects.create(name="J.K.Rowling")
        Book.objects.create(author=tolkien, title="The Hobbit")
        Book.objects.create(author=tolkien, title="The Lord of the Rings")
        Book.objects.create(author=rowling, title="The Prisoner of Azkaban")
        Book.objects.create(author=rowling, title="The Goblet of Fire")

    def setUp(self):
        self.response = self.client.get("/downloadbooks/")
        self.wb = openpyxl.load_workbook(BytesIO(self.response.content))

    def test_body_in_authors(self):
        body = self._get_body("Authors")
        self.assertEqual(
            body,
            [["J.K.Rowling", "J.K.Rowling"], ["J.R.R.Tolkien", "J.R.R.Tolkien"]],
        )


class CustomColumnWidthFactorTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        tolkien = Author.objects.create(name="J.R.R.Tolkien")
        rowling = Author.objects.create(name="J.K.Rowling")
        Book.objects.create(author=tolkien, title="The Hobbit")
        Book.objects.create(author=tolkien, title="The Lord of the Rings")
        Book.objects.create(author=rowling, title="The Prisoner of Azkaban")
        Book.objects.create(author=rowling, title="The Goblet of Fire")

    def setUp(self):
        self.saved_column_width_factor = BooksWorksheet.column_width_factor
        BooksWorksheet.column_width_factor = 1.42
        self.response = self.client.get("/downloadbooks/")
        self.wb = openpyxl.load_workbook(BytesIO(self.response.content))

    def tearDown(self):
        BooksWorksheet.column_width_factor = self.saved_column_width_factor

    def test_column_width(self):
        self.assertAlmostEqual(
            self.wb["Books"].column_dimensions["B"].width,
            len("The prisoner of azkaban") * 1.42,
        )


class RowsWorksheet(Worksheet):
    name = "Rows"
    columns = [{"heading": "Value", "value": lambda value: value}]

    def get_queryset(self):
        return self.parent.rows


class RowsWorkbook(Workbook):
    worksheet_classes = [RowsWorksheet]

    def __init__(self, rows=(), **kwargs):
        self.rows = rows
        super().__init__(**kwargs)


class WorkbookTestCase(SimpleTestCase):
    def test_class_declaration_replaces_default_sheet(self):
        self.assertEqual(RowsWorkbook().sheetnames, ["Rows"])

    def test_saves_rows_from_parent_to_file_like_object(self):
        output = BytesIO()
        RowsWorkbook(rows=["example"]).save(output)
        workbook = openpyxl.load_workbook(output)
        self.assertEqual(list(workbook["Rows"].values), [("Value",), ("example",)])

    def test_constructor_overrides_declared_worksheet_classes(self):
        class OtherWorksheet(RowsWorksheet):
            name = "Other"

        workbook = RowsWorkbook(worksheet_classes=[OtherWorksheet])
        self.assertEqual(workbook.sheetnames, ["Other"])

    def test_worksheet_name_override(self):
        class NamedWorksheet(RowsWorksheet):
            @classmethod
            def get_name(cls):
                return "Custom name"

        workbook = RowsWorkbook(worksheet_classes=[NamedWorksheet])
        self.assertEqual(workbook.sheetnames, ["Custom name"])

    def test_column_override_reads_parent_attributes(self):
        class CustomColumnsWorksheet(RowsWorksheet):
            def get_columns(self):
                return [{"heading": self.parent.heading, "value": lambda row: row}]

        class CustomColumnsWorkbook(RowsWorkbook):
            worksheet_classes = [CustomColumnsWorksheet]
            heading = "Custom heading"

        self.assertEqual(CustomColumnsWorkbook()["Rows"]["A1"].value, "Custom heading")


class CustomWorkbookViewTestCase(SimpleTestCase):
    def test_serializes_workbook_returned_by_override(self):
        class DownloadRows(WorkbookView):
            filename = "rows.xlsx"

            def get_workbook(self):
                return RowsWorkbook(rows=["custom"])

        response = DownloadRows.as_view()(RequestFactory().get("/"))
        workbook = openpyxl.load_workbook(BytesIO(response.content))
        self.assertEqual(workbook["Rows"]["A2"].value, "custom")
