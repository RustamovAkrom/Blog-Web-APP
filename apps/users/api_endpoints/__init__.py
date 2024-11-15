from rest_framework import routers

from .users import UserViewSet, UserProfileViewSet


router = routers.DefaultRouter()
router.register("user", UserViewSet)
router.register("user_profile", UserProfileViewSet)
