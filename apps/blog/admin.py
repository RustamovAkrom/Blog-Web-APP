from django.contrib import admin
from .models import Post, PostComment, PostLike, PostDislike, PostCommentLike

from unfold.admin import ModelAdmin

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ["title", "content", "author", "is_active"]
    search_fields = ["title", "content"]
    list_filter = ["author", "is_active"]
    date_hierarchy = "publisher_at"
    prepopulated_fields = {"slug": ("title",)}


@admin.register(PostComment)
class PostCommentAdmin(ModelAdmin):
    pass


@admin.register(PostLike)
class PostLikeAdmin(ModelAdmin):
    pass


@admin.register(PostDislike)
class PostDislike(ModelAdmin):
    pass


@admin.register(PostCommentLike)
class PostCommentLikeAdmin(ModelAdmin):
    pass
