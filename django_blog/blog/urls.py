# blog/urls.py
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    # ✅ singular paths expected by the checker
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    # (Optional) keep your old plural routes working too
    path("posts/", PostListView.as_view()),
    path("posts/new/", PostCreateView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view()),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view()),
]
