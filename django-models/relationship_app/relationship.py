from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = George Orwell
books_by_author = Book.objects.filter(author__name=author_name)
print(fBooks by {author_name} {[book.title for book in books_by_author]})

# List all books in a library
library_name = Central Library
try
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(fBooks in {library_name} {[book.title for book in books_in_library]})
except Library.DoesNotExist
    print(fLibrary named {library_name} not found.)

# Retrieve the librarian for a library
try
    librarian = library.librarian
    print(fLibrarian of {library_name} {librarian.name})
except Exception as e
    print(Librarian not found or error, e)
