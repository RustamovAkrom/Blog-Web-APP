from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from apps.shared.models import TimestempedAbstractModel
from django.db import models


class User(AbstractUser, TimestempedAbstractModel):
    email = models.EmailField(_("email address"), unique=True)

    @property
    def post_count(self):
        return self.posts.count
    
    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    

class UserProfile(TimestempedAbstractModel):
    user = models.ForeignKey("users.User", models.CASCADE, "user_profiles")
    avatar = models.ImageField(
        _("avatar"), upload_to="avatars/", default="avatars/default/logo.png", blank=True, null=True
    )
    bio = models.CharField(_("bio"), max_length=170)

    class Meta:
        db_table = "user_profiles"
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
