from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from apps.shared.models import TimestempedAbstractModel
from django.db import models


class User(AbstractUser, TimestempedAbstractModel):
    email = models.EmailField(_("email address"), unique=True)

    @property
    def post_count(self):
        return self.posts.count

    def get_user_avatar_url(self):
        return self.profiles.avatar.url

    def get_user_bio(self):
        bio = self.profiles.bio
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
