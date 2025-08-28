# posts/views.py

from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class DefaultPagination(PageNumberPagination):
    page_size = 10

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # required literal
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # required literal
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get("post")
        return qs.filter(post_id=post_id) if post_id else qs

# ---- Feed (function-based) ----
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request):
    following = request.user.following.all()
    posts = Post.objects.filter(author__in=following).order_by('-created_at')  # exact order clause
    data = PostSerializer(posts, many=True, context={"request": request}).data
    return Response(data)
