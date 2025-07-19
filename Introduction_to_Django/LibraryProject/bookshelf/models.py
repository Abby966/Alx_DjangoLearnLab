from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

from bookshelf.models import Book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
book
# <Book: 1984 by George Orwell (1949)>

from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# (1, {'bookshelf.Book': 1})
# <QuerySet []>

from bookshelf.models import Book
Book.objects.all()
# <QuerySet [<Book: 1984 by George Orwell (1949)>]>


from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
# <Book: Nineteen Eighty-Four by George Orwell (1949)>

