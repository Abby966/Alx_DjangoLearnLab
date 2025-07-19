from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # Columns to show
    search_fields = ('title', 'author')                      # Enable search
    list_filter = ('publication_year',)                      # Add filter by year

admin.site.register(Book, BookAdmin)
