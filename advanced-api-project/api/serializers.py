from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book instances.

    Includes custom validation to ensure `publication_year` is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value: int) -> int:
        """
        Ensure the publication year is <= current calendar year.

        Raises:
            serializers.ValidationError: if `value` is in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future (>{current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author instances and nests related books.

    Relationship handling:
        Because Book.author has related_name='books', we can include
        the author's books by declaring a field named 'books' here.

    The nested representation is read-only by default. If you later want
    to create/update books together with authors, you'd override create()
    and update() to handle nested writes explicitly.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
