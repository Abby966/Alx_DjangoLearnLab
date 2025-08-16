from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostsByTagListView,
    PostSearchListView,
)

urlpatterns = [
    # Primary (singular) routes
    path("", PostListView.as_view(), name="post-list"),  # "/" shows the list
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    # Comments
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment-create"),  # pk = post id
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),     # pk = comment id
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),     # pk = comment id

    # Tags + search (support both tag styles)
    path("tags/<slug:slug>/", PostsByTagListView.as_view(), name="posts-by-tag"),
    path("tags/<str:tag_name>/", PostsByTagListView.as_view(), name="posts-by-tag-name"),
    path("search/", PostSearchListView.as_view(), name="search"),

    # Optional plural aliases (handy if you’ve linked them before)
    path("posts/", PostListView.as_view()),
    path("posts/new/", PostCreateView.as_view()),
    path("posts/<int:pk>/", PostDetailView.as_view()),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view()),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view()),
]
