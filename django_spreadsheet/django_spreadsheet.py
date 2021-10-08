from django.http import HttpResponse
from django.views.generic import View


class Worksheet:
    pass


class WorkbookView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse()
