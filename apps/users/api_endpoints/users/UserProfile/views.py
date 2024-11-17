from rest_framework import viewsets

from apps.users.models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

__all__ = ("UserProfileViewSet", )
