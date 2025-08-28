# posts/serializers.py
from rest_framework import serializers
from .models import Post, Like

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at", "updated_at",
                  "likes_count", "is_liked"]
        read_only_fields = ["author", "likes_count", "is_liked"]

    def get_is_liked(self, obj):
        user = self.context["request"].user if "request" in self.context else None
        if not user or not user.is_authenticated:
            return False
        return obj.likes.filter(user=user).exists()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
