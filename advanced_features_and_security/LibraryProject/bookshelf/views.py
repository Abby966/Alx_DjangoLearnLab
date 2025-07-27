from django.http import HttpResponse
from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view_books', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
def index(request):
    return HttpResponse("Welcome to the Book Shelf!")

