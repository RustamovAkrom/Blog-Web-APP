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
        self.assertEqual(
            self.user.id, jwt_refresh.for_user(self.user).access_token["user_id"]
        )

        self.assertEqual(response.status_code, 200)

    def test_api_user_create(self):
        url = "/api/v1/users/user/"

        def _check_user_error_field():
            data = {
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "password_confirm": self.password,
            }
            response = self.client.post(url, data=data)
            response_data = response.json()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response_data["username"][0],
                "A user with that username already exists.",
            )
            self.assertEqual(
                response_data["email"][0],
                "User with this email address already exists.",
            )

        def _check_user_passwords_field():
            data = {
                "username": "Admin2",
                "email": "admin2@example.com",
                "password": "password",
                "password_confirm": "error password",
            }
            response = self.client.post(url, data=data)
            response_data = response.json()

            self.assertEqual(response_data["password"][0], "Password didnt match!")

        def _create_user():
            data = {
                "username": "Admin2",
                "email": "admin2@example.com",
                "password": "password",
                "password_confirm": "password",
            }
            response = self.client.post(url, data=data)
            response_data = response.json()

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_data["username"], data["username"])
            self.assertEqual(response_data["email"], data["email"])
            self.assertEqual(response_data["id"], 2)
            self.assertEqual(response_data["profiles"]["id"], response_data["id"])

        _check_user_error_field()
        _check_user_passwords_field()
        _create_user()

    def test_api_user_update(self):
        pass