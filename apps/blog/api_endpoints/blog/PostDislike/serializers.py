from rest_framework import serializers

from apps.blog.models import PostDislike


class PostDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostDislike
        fields = ["id", "user", "post"]
