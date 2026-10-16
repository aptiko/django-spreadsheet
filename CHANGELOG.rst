=======
History
=======

2.0.0 (2026-10-16)
------------------

Backwards-incompatible changes:

* ``WorkbookView``'s ``worksheets`` attribute has been renamed to
  ``worksheet_classes``.

* ``Worksheet``'s ``view`` and ``request`` attributes have been removed.
  Instead, use the openpyxl's ``Worksheet.parent`` attribute to access the
  workbook. If you need to access the view or the request object, you should
  customize ``Workbook`` or ``WorkbookView.get_workbook()`` so that the
  necessary data is accessible by the workbook through custom attributes.

Other changes:

* Added a ``Workbook`` class (useful if you need to generate workbooks outside
  of a Django view.)

1.4.0 (2024-12-18)
------------------

* Added the get_name() and get_columns() methods of Worksheet.

Note: 1.3.0 was a short-lived version released in the same day, of which
get_columns() was a class method, but this didn't work well.

1.2.1 (2024-04-22)
------------------

* Updated requirements for compatibility with Django 4 and 5.

1.2.0 (2023-10-21)
------------------

* Added attribute Worksheet.view.

1.1.1 (2023-09-30)
------------------

* Fixed error when specifying partial functions as "value" in
  Worksheet.columns.

1.1.0 (2022-10-02)
------------------

* Now accepts methods as "value" in Worksheet.columns.

1.0.0 (2021-10-09)
------------------

Initial release.
