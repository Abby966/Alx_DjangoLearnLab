# api/models.py
from django.db import models

class Author(models.Model):
    """
    Represents a book author.
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """
    Represents a book written by a specific author.
    One Author -> many Books via ForeignKey.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,              # you can also use "Author" (string) as a forward reference
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
