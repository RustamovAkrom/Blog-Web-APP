from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.users.models import UserProfile
from apps.users.permissions import IsOwnerPermission
from .serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsAdminUser(), IsOwnerPermission()]

__all__ = ("UserProfileViewSet", )
