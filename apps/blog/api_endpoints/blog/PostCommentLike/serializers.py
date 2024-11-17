from rest_framework import serializers

from apps.blog.models import PostCommentLike
from apps.users.models import User


class MiniPostCommentLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "created_at", "updated_at"]


class MiniPostCommentLikePostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "post", "message", "created_at", "updated_at"]


class PostCommentLikeSerializer(serializers.ModelSerializer):
    user = MiniPostCommentLikeUserSerializer(read_only=True)
    comment = MiniPostCommentLikePostCommentSerializer(read_only=True)
    
    class Meta:
        model = PostCommentLike
        fields = ["id", "user", "comment"]
