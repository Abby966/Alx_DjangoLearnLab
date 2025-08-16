from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at")  # removed published_date
    search_fields = ("title", "content", "author__username")
    list_filter = ("author", "created_at")  # must be real model fields
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
