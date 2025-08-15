from django.shortcuts import render
# api/views.py
from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

# Create your views here.
