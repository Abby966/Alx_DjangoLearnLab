from django.db import models


class Author(models.Model):
    """
    Represents a book author.

    Fields:
        name (str): The human-readable name of the author.

    Purpose:
        Authors have a one-to-many relationship with Book (an Author can have many Books).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        # Useful for admin & shell displays
        return self.name


class Book(models.Model):
    """
    Represents a book written by a specific author.

    Fields:
        title (str): The title of the book.
        publication_year (int): The year the book was published.
        author (FK): ForeignKey to Author establishing one-to-many (Author -> Books).

    Notes:
        related_name='books' lets us access an author's books via author.books.
        This simplifies nested serialization in AuthorSerializer.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

# Create your models here.
