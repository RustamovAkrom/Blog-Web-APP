from rest_framework import serializers

from apps.blog.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["id", "user", "post"]
