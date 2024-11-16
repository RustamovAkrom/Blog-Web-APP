from rest_framework import serializers

from apps.users.models import User, UserProfile


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
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name", 
            "last_name", 
            "username",
            "email", 
            "password",
            "password_confirm",
            "is_active", 
            "is_superuser",
            "is_staff",
            "post_count",
            "profiles",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        "Confirmation passwords"

        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password didnt match!"})
        return attrs
    

    def create(self, validated_data):
        "Save a hashed password"

        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
