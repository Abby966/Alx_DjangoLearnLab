from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('date_of_birth', 'profile_photo')}),
    )

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # Columns to show
    search_fields = ('title', 'author')                      # Enable search
    list_filter = ('publication_year',)                      # Add filter by year

admin.site.register(Book, BookAdmin)
