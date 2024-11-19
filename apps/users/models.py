from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.shared.models import TimestempedAbstractModel
from .utils import processor_iamge


class User(TimestempedAbstractModel, AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    @property
    def post_count(self):
        return self.posts.count

    def get_user_avatar_url(self) -> str:
        return str(self.profiles.avatar.url)

    def get_user_bio(self) -> str:
        bio = str(self.profiles.bio)
        if bio:
            return bio
        return ""

    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return self.username


class UserProfile(TimestempedAbstractModel):
    user = models.OneToOneField(
        "users.User",
        models.CASCADE,
        related_name="profiles",
    )
    avatar = models.ImageField(
        _("avatar"),
        upload_to="avatars/",
        default="avatars/default/logo.png",
        max_length=250,
        blank=True,
        null=True,
    )
    bio = models.CharField(_("bio"), max_length=170, blank=True, null=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        processor_iamge(self.avatar.path)
