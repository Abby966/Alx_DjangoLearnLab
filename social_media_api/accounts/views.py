# accounts/views.py

from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """Follow another user by id."""
    if request.user.id == user_id:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    request.user.following.add(target)  # update following relationship
    return Response(
        {
            "detail": f"You now follow {target.username}.",
            "following_count": request.user.following.count(),
            "followers_count": target.followers.count(),
        },
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """Unfollow another user by id."""
    if request.user.id == user_id:
        return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    request.user.following.remove(target)  # update following relationship
    return Response(
        {
            "detail": f"You unfollowed {target.username}.",
            "following_count": request.user.following.count(),
            "followers_count": target.followers.count(),
        },
        status=status.HTTP_200_OK,
    )
