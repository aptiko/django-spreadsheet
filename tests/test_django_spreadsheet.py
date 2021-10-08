#!/usr/bin/env python

from django.test import TestCase

import django_spreadsheet


class WorkbookViewTestCase(TestCase):
    def test_view(self):
        response = self.client.get("/downloadbooks/")
        self.assertEqual(response.status_code, 200)
