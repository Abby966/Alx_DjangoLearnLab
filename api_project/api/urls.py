from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet  # keep BookList for old endpoint if needed

# Create router
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Old endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # CRUD endpoints
    path('', include(router.urls)),
]
