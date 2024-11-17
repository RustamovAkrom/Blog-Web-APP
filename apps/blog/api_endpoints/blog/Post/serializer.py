from rest_framework import serializers

from apps.blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title", 
            "get_absolute_url",
            "status",
            "description",
            "publisher_at",
            "is_active",
            "author",
            "like_count",
            "dislike_count",
            "comment_count",
            "watching",
            "created_at",
            "updated_at",
        ]