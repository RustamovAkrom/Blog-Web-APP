from apps.users.models import User, UserProfile

from rest_framework import serializers


class MiniUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "avatar",
            "bio",
        ]

        
class UserSerializer(serializers.ModelSerializer):
    profiles = MiniUserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name", 
            "last_name", 
            "username",
            "email", 
            "is_active", 
            "is_superuser",
            "is_staff",
            "post_count",
            "profiles",
        ]
