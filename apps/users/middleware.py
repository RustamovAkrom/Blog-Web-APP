from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache


User = get_user_model()


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # If admin auth for session
        if request.path.startswith("/admin"):
            return

        access_token = request.COOKIES.get("access_token")

        if not access_token:
            request.user = AnonymousUser()
            return

        cached_user = cache.get(access_token)
        if cached_user:
            request.user = cached_user
            return

        try:
            token = AccessToken(access_token)
            user_id = token["user_id"]
            user = User.objects.get(id=user_id)

            cache.set(access_token, user, timeout=60 * 15)
            request.user = user
        except (TokenError, User.DoesNotExist):
            request.user = AnonymousUser()
