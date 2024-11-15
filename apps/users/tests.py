from django.test import TestCase
from django.urls import reverse

from .models import User, UserProfile


class TestUsers(TestCase):

    def test_user_register_page(self):
        response = self.client.get(reverse("users:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register.html")
        self.assertContains(response, "Register")
        # self.assertRedirects(response, reverse("users:login"))

    def test_user_login_page(self):
        response = self.client.get(reverse("users:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertContains(response, "Login")
        # self.assertRedirects(response, reverse("blog:home"))