from django.contrib import admin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "post_count"]
    search_fields = ["first_name", "last_name", "username"]
    list_display_links = ["username"]

    def get_post_count(self):
        return self.post_count


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
