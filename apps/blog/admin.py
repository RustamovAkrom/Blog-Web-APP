from django.contrib import admin
from .models import Post, PostComment, PostLike, PostDislike, PostCommentLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "author", "is_active"]
    search_fields = ["title", "content"]
    list_filter = ["author", "is_active"]
    date_hierarchy = "publisher_at"
    prepopulated_fields = {"slug": ("title",)}


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(PostDislike)
class PostDislike(admin.ModelAdmin):
    pass


@admin.register(PostCommentLike)
class PostCommentLikeAdmin(admin.ModelAdmin):
    pass
