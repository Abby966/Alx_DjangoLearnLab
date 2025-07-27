from django.http import HttpResponse
from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
def index(request):
    return HttpResponse("Welcome to the Book Shelf!")

