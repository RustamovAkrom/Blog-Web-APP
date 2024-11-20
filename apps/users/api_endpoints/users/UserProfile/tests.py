from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import UserProfile, User


class UserProfileApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.username = "Admin"
        self.email = "admin@gmail.com"
        self.password = "password"
        user = User.objects.create(
            username=self.username,
            email=self.email,
        )
        user.set_password(self.password)
        user.save()
        self.user = user
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        return super().setUp()
    
    