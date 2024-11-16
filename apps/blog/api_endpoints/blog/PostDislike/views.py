from django.shortcuts import get_object_or_404

from rest_framework import viewsets, response, status, permissions

from apps.blog.models import PostDislike, PostLike, Post
from .serializers import PostDislikeSerializer


class PostDislikeViewSet(viewsets.ModelViewSet):
    queryset = PostDislike.objects.all()
    serializer_class = PostDislikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post")
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        PostLike.objects.filter(post=post, user=user).delete()

        existing_dislike = PostDislike.objects.filter(post=post, user=user)
        if existing_dislike.exists():
            existing_dislike.delete()
            return response.Response({"message": "Dislike removed"}, status=status.HTTP_200_OK)
        
        dislike = PostDislike.objects.create(post=post, user=user)
        serializer = self.get_serializer(dislike)

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
    

__all__ = ("PostDislikeViewSet", )
