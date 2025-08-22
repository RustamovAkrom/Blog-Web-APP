from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.shared.models import TimestempedAbstractModel
from .utils import processor_iamge


class User(TimestempedAbstractModel, AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    @property
    def post_count(self) -> int:
        """Количество постов пользователя"""
        return getattr(self, "posts", None).count() if hasattr(self, "posts") else 0

    def get_user_avatar_url(self) -> str:
        """Безопасно возвращает URL аватара"""
        if hasattr(self, "profiles") and self.profiles.avatar:
            return self.profiles.avatar.url
        return "/media/avatars/default/logo.png"

    def get_user_bio(self) -> str:
        """Безопасно возвращает bio"""
        if hasattr(self, "profiles") and self.profiles.bio:
            return self.profiles.bio
        return ""

    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        """Автоматически создаём профиль при сохранении юзера"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not hasattr(self, "profiles"):
            UserProfile.objects.create(user=self)


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
        if self.avatar:  # обработка изображения только если оно реально есть
            try:
                processor_iamge(self.avatar.path)
            except (FileNotFoundError, ValueError):
                pass
