# api/views.py
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Filtering:  ?title=&publication_year=&author=
    Searching:  ?search=  (title, author name)
    Ordering:   ?ordering=title | -title | publication_year | -publication_year | id | -id
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["title", "publication_year", "author"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year", "id"]
    ordering = ["title"]

class BookDetailView(generics.RetrieveAPIView):
    """GET /api/books/<pk>/"""
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "pk"

class BookCreateView(generics.CreateAPIView):
    """POST /api/books/create/ (auth)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer): serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """PUT/PATCH /api/books/update/<pk>/ (auth)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    def perform_update(self, serializer): serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """DELETE /api/books/delete/<pk>/ (auth)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
