from rest_framework import viewsets, permissions

from apps.blog.models import PostComment
from .serializers import PostCommentSerializer


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all().order_by("-created_at")
    serializer_class = PostCommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]   
    
__all__ = ("PostCommentViewSet", )
