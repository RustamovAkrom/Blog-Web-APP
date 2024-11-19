from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from django.urls import reverse

from apps.users.models import User

# Authorizations
# self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

class UsersApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.username = "Admin"
        self.email = "admin@example.com"
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
    
    def test_api_tokens(self):
        data = {
            "username": "Admin",
            "password": "password",
        }
        response = self.client.post(reverse("token_obtain_pair"), data=data)
        tokens = dict(response.json())
        refresh = tokens.get("refresh")
        access = tokens.get("access")

        # Test jwt access token
        jwt_access = AccessToken(access)
        self.assertEqual(self.user.id, jwt_access["user_id"])

        # Test jwt refresh token
        jwt_refresh = RefreshToken(refresh)
        self.assertEqual(self.user.id, jwt_refresh.for_user(self.user).access_token["user_id"])

        self.assertEqual(response.status_code, 200)

    # def test_api_user_create(self):
    #     url = "/api/v1/users/user/"
    #     def check_user():
    #         data = {
    #             "username": "Admin2",
    #             "email": "admin2@example.com",
    #             "password": "password",
    #             "password_confirm": "password"
    #         }

    #     invalid_data = {
    #         "username": self.username,
    #         "email": self.email,
    #         "password": self.password,
    #         "password_confirm": self.password
    #     }
        
    #     response = self.client.post(url, data=valid_data)
        

    #     print(response.status_code)
    #     print(response.json())

