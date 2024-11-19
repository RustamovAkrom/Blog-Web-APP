from rest_framework import viewsets, permissions
from rest_framework_simplejwt import authentication

from apps.users.models import User
from .serializers import UserSerializer
from apps.users.permissions import IsOwnerPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.JWTAuthentication]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]

        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [
                permissions.IsAuthenticated(),
                permissions.IsAdminUser,
                IsOwnerPermission(),
            ]

        return [permissions.IsAuthenticated()]


__all__ = ("UserViewSet",)
