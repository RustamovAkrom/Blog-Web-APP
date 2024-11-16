from rest_framework import viewsets, permissions

from apps.blog.models import PostCommentLike
from .serializers import PostCommentLikeSerializer


class PostCommentLikeViewSet(viewsets.ModelViewSet):
    queryset = PostCommentLike.objects.all().order_by("-id")
    serializer_class = PostCommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

__all__ = ("PostCommentLikeViewSet", )
