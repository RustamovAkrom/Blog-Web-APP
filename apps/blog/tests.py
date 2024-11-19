from datetime import datetime

from django.test import TestCase
from apps.users.models import User
from apps.blog.models import Post
from django.urls import reverse
from apps.users.forms import RegisterForm
from .forms import PostCreateUpdateForm
from .choices import StatusChoice


class TestBlog(TestCase):
    def setUp(self):
        user = User.objects.create(
            first_name="Admin",
            last_name="Adminovich",
            username="Admin",
            email="saydulapolatov456@gmail.com",
        )

        user.set_password("2007")
        user.save()
        self.user = user

        post = Post.objects.create(
            title="PostTitle1d",
            description="PostDescription1",
            content="PostContent1",
            publisher_at=datetime.now().strftime("%Y-%m-%d"),
            author=self.user,
            is_active=True,
        )
        self.post = post

    def test_home_page(self):
        response = self.client.get(reverse("blog:home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse("blog:about"))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page(self):
        response = self.client.get(reverse("blog:contacts"))
        self.assertEqual(response.status_code, 200)

    def test_post_detil(self):
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post.slug}))
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.post.author.username)
        self.assertTrue(self.post.is_active, "True")

    def test_PostCreateUpdateForm_forms(self):
        form_data = {
            "title": "PostTitle1",
            "description": "PostDescription1",
            "content": "PostContent1",
            "is_active": True,
            "author": self.user,
            "status": StatusChoice.PUBLISHED.value
        }

        form = PostCreateUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form(self):
        user_create_form_data = {
            "username": "Saydula",
            "first_name": "Sayid",
            "last_name": "Movlonov",
            "password1": "Sayid",
            "password2": "Sayid",
            "email": "sayidmovlonov34@gmail.com",
            "avatar": "C:/Users/user/Pictures/Screenshots homevork/Снимок экрана 2024-02-08 193246.png",
        }
        form = RegisterForm(data=user_create_form_data)
        self.assertTrue(form.is_valid())
