from django.shortcuts import get_object_or_404

from rest_framework import viewsets, response, status, permissions

from apps.blog.models import PostLike, PostDislike, Post
from .serializers import PostLikeSerializer


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post")
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        PostDislike.objects.filter(post=post, user=user).delete()

        existing_like = PostLike.objects.filter(post=post, user=user)
        if existing_like.exists():
            existing_like.delete()
            return response.Response({"message": "Like removed"}, status=status.HTTP_200_OK)
        
        like = PostLike.objects.create(post=post, user=user)
        serializer = self.get_serializer(like)

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

__all__ = ("PostLikeViewSet", )
