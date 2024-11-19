from django.test import TestCase
from django.urls import reverse

from .models import User, UserProfile
from .services import generate_jwt_tokens
from .forms import RegisterForm, LoginForm

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class TestUsers(TestCase):
    def setUp(self):
        self.username = "Admin"
        self.is_active=True
        self.email = "admin@example.com",
        self.password = "password"

        user = User.objects.create(
            username=self.username, 
            is_active=self.is_active, 
            email=self.email
        )
        user.set_password(self.password)
        user.save()

        self.user = user

    def test_user_creating_profile_exists(self):
        profile = UserProfile.objects.filter(pk=self.user.profiles.pk)
        self.assertTrue(profile.exists())

    def test_user_register_page(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register.html")
        self.assertContains(response, "Register")

    def test_user_login_page(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertContains(response, "Login")

    def test_user_logout_page(self):
        data = {
            "username": self.username,
            "password": self.password,
        }
        # Authorization
        self.client.post(reverse("users:login"), data=data)

        response = self.client.get(reverse("users:logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/logout.html")
        self.assertContains(response, "Logout")

    def test_user_profile_page(self):
        response = self.client.get(reverse("users:user_profile", kwargs={"username": self.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/profile.html")
        self.assertContains(response, self.user.username)

    def test_RegisterForm(self):
        form_data = {
            "username": "Admin1",
            "password1": "password1",
            "password2": "password1",
            "email": "admin1@example.com",
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_LoginForm(self):
        form_data = {
            "username": "Admin1",
            "password": "password1",
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration(self):
        data = {
            "username": "Admin1",
            "password1": "password1",
            "password2": "password1",
            "email": "admin1@example.com",
        }
        response = self.client.post(reverse("users:register"), data=data)
        self.assertEqual(response.status_code, 302) # Redirecting
        self.assertRedirects(response, reverse("users:login"))
        
    def test_authorization(self):
        data = {
            "username": self.username,
            "password": self.password,
        }
        
        response = self.client.post(reverse("users:login"), data=data)

        refresh_token = response.client.cookies.get("refresh_token").value
        access_token = response.client.cookies.get("access_token").value
        
        self.assertEqual(response.status_code, 302) # Redirecting
        self.assertRedirects(response, reverse("blog:home"))

        access_token = AccessToken(access_token)
        refresh_token = RefreshToken(refresh_token)

        user_id = access_token["user_id"]
        user_in_db = User.objects.filter(id=user_id)
        
        user_in_refresh_id = refresh_token.for_user(user_in_db.first()).access_token["user_id"]

        self.assertTrue(user_in_db.exists())
        self.assertEqual(self.user.id, user_in_db.first().id)
        self.assertEqual(self.user.id, user_in_refresh_id)

    def test_logout(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        # Authorization
        response = self.client.post(reverse("users:login"), data=data)

        refresh_token_before = response.client.cookies.get("refresh_token").value
        access_token_before = response.client.cookies.get("access_token").value

        response = self.client.post(reverse("users:logout"))

        refresh_token_after = response.client.cookies.get("refresh_token").value
        access_token_after = response.client.cookies.get("access_token").value

        self.assertNotEqual(refresh_token_before, refresh_token_after)
        self.assertNotEqual(access_token_before, access_token_after)

