=========
Reference
=========

WorkbookView
============

.. class:: django_spreadsheet.WorkbookView

   Base class for a Django view whose response is an xlsx workbook. You
   need to specify :attr:`~django_spreadsheet.filename` and
   :attr:`~django_spreadsheet.worksheets`.

   .. attribute:: django_spreadsheet.WorkbookView.filename

      The filename of the workbook. This will be specified in the
      ``Content-disposition`` header of the response, so it will be the
      filename that the browser will use to save the workbook as.

   .. attribute:: django_spreadsheet.WorkbookView.worksheets

      A list of :class:`~django_spreadsheet.Worksheet` classes. The
      returned workbook will contain these worksheets.

Worksheet
=========

.. class:: django_spreadsheet.Worksheet

   Base class for worksheets.

   Do not attempt to instantiate :class:`~django_spreadsheet.Worksheet`
   objects directly. They are only meant to be instantiated
   automatically by :class:`~django_spreadsheet.WorkbookView`, which
   will also set ``self.request`` to the Django request object. This can
   come in handy in
   :meth:`~django_spreadsheet.Worksheet.get_queryset()`.

   .. attribute:: django_spreadsheet.Worksheet.model

      Mandatory. The model that will be queried to populate the worksheet.

   .. attribute:: django_spreadsheet.Worksheet.name

      Mandatory unless :meth:`get_name` is overridden. The name of the
      worksheet—it will be used in the worksheet tab.

   .. classmethod:: django_spreadsheet.Worksheet.get_name

      Returns the name of the worksheet, which will be used in the
      worksheet tab. The default merely returns :attr:`name`. Override
      if you need a more complicated workflow, such as a localized name.

   .. method:: django_spreadsheet.Worksheet.get_queryset()

      Optional. The default returns ``self.model.objects.all()``.
      Override it if you need a different queryset.

   .. attribute:: django_spreadsheet.Worksheet.columns

      Mandatory unless :meth:`get_columns` is overridden. It is a list
      of dictionaries that specify the columns of the worksheet. Each
      dictionary has the following items:

      .. data:: heading

         The column heading, a string.

      .. data:: value

         A string or function describing the value the cell will have
         for each row.

         If it is a string, then it is interpreted as a dotted path. For
         example, if :data:`value` is "author.name", then for each item
         ``obj`` of the queryset the cell value will be
         ``obj.author.name``.

         If it is a one-argument function, it receives the queryset
         item and returns the cell value.  Thus, ``"author.name"`` and
         ``lambda obj: obj.author.name`` will have the same result when
         used as the :data:`value`. In this case, prefer the first
         format. Use a function only for the cases when a string cannot
         do what you want.

         If the function is a two-argument function, it receives the
         :class:`~django_spreadsheet.Worksheet` object as the first
         argument and the queryset item as the second argument, and
         returns the cell value. Thus you can specify
         :class:`~django_spreadsheet.Worksheet` methods in
         :attr:`~django_spreadsheet.Worksheet.columns`, for example::

            import django_spreadsheet

            from myapp import models

            class MyWorksheet(django_spreadsheet.Worksheet):
                model = models.Book
                name = "Books"

                def get_book_title(self, book):
                    if self.request.user.is_authenticated:
                        return self.book.title
                    else:
                        return "Redacted"

                columns = [
                    {"heading": "Title", "value": get_book_title},
                ]

         Do this only if you need to use ``self``; otherwise use one of
         the other forms.

   .. method:: django_spreadsheet.Worksheet.get_columns

      Returns a list of dictionaries with the format described in
      :attr:`columns`, specifying the columns of the worksheet. The
      default merely returns :attr:`columns`. Override if you need a
      more complicated workflow.

   .. attribute:: django_spreadsheet.Worksheet.column_width_factor

      Optional. A number specifying how large to make column widths.

      django-spreadsheet attempts to "autofit" columns. However, in order to
      actually autofit columns, the spreadsheet would need to be rendered.
      django-spreadsheet (and the openpyxl library on which it is based) does
      not have rendering capabilities, therefore it cannot really autofit
      columns.

      The best we can do is find the max character length for each column and
      multiply it with a number, namely
      :attr:`~django_spreadsheet.Worksheet.column_width_factor`. The default is
      1.23, which has been found with experimentation to provide good results.

   .. attribute:: django_spreadsheet.Worksheet.view

      When a :class:`~django_spreadsheet.WorkbookView` creates a
      :class:`~django_spreadsheet.Worksheet` object, it creates this attribute
      that points to the view instance.  One use case of this is if a workbook
      (i.e. a :class:`django_spreadsheet.WorkbookView`) has many worksheets
      that both need the same queries. In that case, in order to avoid making
      the same queries multiple times, they can be stored in the view and
      accessed from the worksheets.

   .. attribute:: django_spreadsheet.Worksheet.request

      When a :class:`~django_spreadsheet.WorkbookView` creates a
      :class:`~django_spreadsheet.Worksheet` object, it creates this attribute
      that points to request object.
