from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()


class JWTAdminAuthentication(ModelBackend):
    def authenticate(self, request):
        # get access token in cookies
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None
        
        try:
            # Decode token
            token = AccessToken(access_token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)
            return (user, None)
        except (TokenError, ObjectDoesNotExist):
            return None
