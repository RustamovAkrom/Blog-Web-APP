from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.shared.models import TimestempedAbstractModel
from apps.shared.utils import get_random_text
from .managers import PublishedManager
from .choices import StatusChoice


class Post(TimestempedAbstractModel):

    title = models.CharField(_("title"), max_length=120, db_index=True)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, db_index=True)
    status = models.CharField(
        _("status"),
        max_length=2,
        choices=StatusChoice.choices,
        default=StatusChoice.DRAFT.value,
    )
    description = models.CharField(
        _("description"), max_length=300, blank=True, null=True
    )
    content = models.TextField(_("content"))
    publisher_at = models.DateField(_("publisher at"))
    is_active = models.BooleanField(_("active"), default=True)
    author = models.ForeignKey("users.User", models.CASCADE, "posts", db_index=True)
    watching = models.BigIntegerField(_("watching"), default=0)

    objects = models.Manager()
    published = PublishedManager()

    def delete(self, *args, **kwargs):
        self.post_comments.all().delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "posts"
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def get_author_avatar_url(self):
        return self.author.profiles.avatar.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{ slugify(self.title) }-{ get_random_text() }"
        return super().save(*args, **kwargs)

    def like_count(self):
        return self.post_likes.count()

    def dislike_count(self):
        return self.post_dislikes.count()

    def comment_count(self):
        return self.post_comments.count()

    def __str__(self) -> str:
        return self.title


class PostLike(models.Model):
    user = models.ForeignKey("users.User", models.CASCADE, "post_likes", db_index=True)
    post = models.ForeignKey("blog.Post", models.CASCADE, "post_likes", db_index=True)

    def __str__(self) -> str:
        return f"{self.user} -(👍🏼)- {self.post}"


class PostDislike(models.Model):
    user = models.ForeignKey(
        "users.User", models.CASCADE, "post_dislikes", db_index=True
    )
    post = models.ForeignKey(
        "blog.Post", models.CASCADE, "post_dislikes", db_index=True
    )

    def __str__(self) -> str:
        return f"{self.user} -(👎🏼)- {self.post}"


class PostComment(TimestempedAbstractModel):
    user = models.ForeignKey(
        "users.User", models.CASCADE, "post_comments", db_index=True
    )
    post = models.ForeignKey(
        "blog.Post", models.CASCADE, "post_comments", db_index=True
    )
    message = models.TextField(_("message"))

    def __str__(self) -> str:
        return f"{self.user} -(💬)- {self.post}"


class PostCommentLike(models.Model):
    user = models.ForeignKey(
        "users.User", models.CASCADE, "post_comment_likes", db_index=True
    )
    comment = models.ForeignKey(
        "blog.PostComment", models.CASCADE, "post_comment_likes", db_index=True
    )

    def __str__(self) -> str:
        return f"{self.user} -(💬, 👍🏼)- {self.comment}"
