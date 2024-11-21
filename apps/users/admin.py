from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

from unfold.admin import ModelAdmin

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ["username", "post_count"]
    search_fields = ["first_name", "last_name", "username"]
    list_display_links = ["username"]

    def get_post_count(self):
        return self.post_count


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    pass
