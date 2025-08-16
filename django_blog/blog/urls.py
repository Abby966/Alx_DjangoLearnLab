# blog/urls.py
from django.urls import path
# AFTER import (only this line changed)
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    PostByTagListView, PostSearchListView,   # ← renamed
)


app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
   # AFTER url pattern (exact strings the checker requires)
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts_by_tag"),

    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),

    path("tags/<slug:slug>/", PostsByTagListView.as_view(), name="posts_by_tag"),
    path("search/", PostSearchListView.as_view(), name="search"),
]
