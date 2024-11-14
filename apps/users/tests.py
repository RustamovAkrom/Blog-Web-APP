from django.test import TestCase

from .models import User, UserProfile


class TestUsers(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            username="User",
            email="user@example.com",
            password="password"
        )
        return super().setUp()
    
    