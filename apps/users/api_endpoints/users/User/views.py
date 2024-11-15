from apps.users.models import User
from .serializers import UserSerializer

from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

__all__ = ("UserViewSet", )
