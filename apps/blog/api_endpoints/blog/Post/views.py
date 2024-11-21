from rest_framework import viewsets, permissions

from apps.blog.models import Post
from .serializer import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published.all().order_by("-created_at")
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


__all__ = ("PostViewSet",)
