import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library

def run_queries():
    # Query all books by a specific author
    author_name = "Jane Austen"
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"Books by {author.name}: {[book.title for book in books]}")
    except Author.DoesNotExist:
        print(f"No author named {author_name}")

    # List all books in a library
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library.name}: {[book.title for book in books]}")
    except Library.DoesNotExist:
        print(f"No library named {library_name}")

    # Retrieve the librarian for a library
    try:
        librarian = library.librarian
        print(f"Librarian for {library.name}: {librarian.name}")
    except Exception:
        print(f"Librarian not assigned to {library.name}")

if __name__ == '__main__':
    run_queries()
