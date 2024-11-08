from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from apps.shared.models import TimestempedAbstractModel


class User(AbstractUser, TimestempedAbstractModel):
    avatar = models.ImageField(
        upload_to="avatars/", null=True, default="avatars/default/logo.png"
    )

    @property
    def post_count(self):
        return self.posts.count


class Post(TimestempedAbstractModel):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField()
    publisher_at = models.DateField()
    is_active = models.BooleanField(default=False)
    author = models.ForeignKey("User", models.CASCADE, "posts")
    watching = models.BigIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def get_author_avatar_url(self):
        return self.author.avatar.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def like_count(self):
        return self.post_likes.count()
    
    def comment_count(self):
        return self.post_comments.count()
    
    def __str__(self) -> str:
        return self.title
    

class PostLike(models.Model):
    user = models.ForeignKey("User", models.CASCADE, "post_likes")
    post = models.ForeignKey("Post", models.DO_NOTHING, "post_likes")

    def __str__(self) -> str:
        return f"{self.user} -(👍🏼)- {self.post}"
    
    
class PostDislike(models.Model):
    user = models.ForeignKey("User", models.CASCADE, "post_dislikes")
    post = models.ForeignKey("Post", models.DO_NOTHING, "post_dislikes")

    def __str__(self) -> str:
        return f"{self.user} -(👎🏼)- {self.post}"
    

class PostComment(TimestempedAbstractModel):
    user = models.ForeignKey("User", models.CASCADE, "post_comments")
    post = models.ForeignKey("Post", models.DO_NOTHING, "post_comments")
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.user} -(💬)- {self.post}"
    

class PostCommentLike(models.Model):
    user = models.ForeignKey("User", models.CASCADE, "post_comment_likes")
    comment = models.ForeignKey("PostComment", models.DO_NOTHING, "post_comment_likes")

    def __str__(self) -> str:
        return f"{self.user} -(💬, 👍🏼)- {self.comment}"