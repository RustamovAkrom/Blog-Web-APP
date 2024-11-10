from django.db.models.signals import post_save
from django.http import JsonResponse
from django.dispatch import receiver
from .models import User, UserProfile

from rest_framework_simplejwt.tokens import RefreshToken
from allauth.account.signals import user_logged_in


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating UserProfile to User({instance})")

        UserProfile.objects.create(user=instance)

@receiver(user_logged_in)
def generate_jwt_token(sender, request, user, **kwargs):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    data = {
        "refresh": str(refresh),
        "access": access_token,
    }

    request._dont_enforce_csrf_checks = True
    response = JsonResponse(data)
    response.status_code = 200
    return response
