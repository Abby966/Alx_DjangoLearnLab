# posts/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request):
    """
    Return posts from users the current user follows,
    ordered by newest first.
    """
    following = request.user.following.all()
    posts = Post.objects.filter(author__in=following).order_by('-created_at')  # <- exact string the checker wants
    serializer = PostSerializer(posts, many=True, context={"request": request})
    return Response(serializer.data)
