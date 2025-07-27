from django.http import HttpResponse
from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import permission_required
from .forms import ExampleForm

def example_form_view(request):
    form = ExampleForm()
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Do something with the valid data (e.g., search books)
            title = form.cleaned_data['title']
            # For now, just pass it to the template
            return render(request, 'form_example.html', {'form': form, 'title': title})
    return render(request, 'form_example.html', {'form': form})

# ✅ Good (safe from SQL injection)
Book.objects.filter(title__icontains=query)

@permission_required('bookshelf.can_view_books', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
def index(request):
    return HttpResponse("Welcome to the Book Shelf!")

