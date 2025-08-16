# blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "content", "tags__name")
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("title",)}
