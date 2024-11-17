from rest_framework import serializers

from apps.blog.models import PostComment, Post
from apps.users.models import User


class MiniPostCommentUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "created_at", "updated_at"]


class MiniPostCommentPost(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "created_at", "updated_at"]


class PostCommentSerializer(serializers.ModelSerializer):
    user = MiniPostCommentUser(read_only=True)
    comment = MiniPostCommentPost(read_only=True)

    class Meta:
        model = PostComment
        fields = ["id", "user", "comment", "created_at", "updated_at"]
