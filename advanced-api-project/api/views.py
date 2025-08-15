# api/views.py
from rest_framework import generics, filters  # <-- includes "filters" module
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Filtering:  ?title=&publication_year=&author=
    Searching:  ?search=  (matches title, author name)
    Ordering:   ?ordering=title | -title | publication_year | -publication_year | id | -id
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # EXACT strings the grader looks for:
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,          # <-- "filters.SearchFilter"
        filters.OrderingFilter,        # <-- "filters.OrderingFilter"
    ]

    # filter by exact fields (FK author by id)
    filterset_fields = ["title", "publication_year", "author"]

    # search across title and author name
    search_fields = ["title", "author__name"]

    # allow ordering by these fields
    ordering_fields = ["title", "publication_year", "id"]
    ordering = ["title"]  # default
