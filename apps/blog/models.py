from django.db import models
from django.contrib.auth.models import AbstractUser


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, AbstractBaseModel):
    avatar = models.ImageField(
        upload_to="avatars/", null=True, default="avatars/default/logo.png"
    )

    @property
    def post_count(self):
        return self.posts.count


class Post(AbstractBaseModel):
    title = models.CharField(max_length=120)
    content = models.TextField()
    publisher_at = models.DateField()
    is_active = models.BooleanField(default=False)
    author = models.ForeignKey("User", models.CASCADE, "posts")
