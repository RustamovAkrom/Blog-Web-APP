from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model


User = get_user_model()


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")

        if access_token:
            try:
                token = AccessToken(access_token)
                user_id = token['user_id']
                request.user = User.objects.get(id=user_id)
            except Exception as e:
                request.user = None
                