from django.contrib import admin
from .models import Post, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display    = ['username', 'post_count']
    search_fields   = ['first_name', 'last_name', 'username']
    list_display_links  = ['username']

    def get_post_count(self): return self.count


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display    = ['title', 'content', 'author', 'is_active']
    search_fields   = ['title', 'content']
    list_filter     = ['author', 'is_active']
    date_hierarchy = 'publisher_at'
