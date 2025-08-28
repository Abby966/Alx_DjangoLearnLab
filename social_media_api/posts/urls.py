# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, feed, like_post, unlike_post

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", feed, name="feed"),                           # /api/feed/
    path("posts/<int:pk>/like/", like_post, name="post-like"),  # /api/posts/<pk>/like/
    path("posts/<int:pk>/unlike/", unlike_post, name="post-unlike"),
]
