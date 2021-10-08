from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]


class Book(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        ordering = ["author", "title"]
