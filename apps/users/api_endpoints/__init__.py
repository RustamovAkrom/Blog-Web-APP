from rest_framework import routers

from .users import UserViewSet, UserProfileViewSet


router = routers.DefaultRouter()
router.register("user", UserViewSet, basename="user")
router.register("user_profile", UserProfileViewSet, basename="user_profile")
