from django.http import HttpResponse, HttpRequest
from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    access_token["user_id"] = user.id

    access_token = str(access_token)
    refresh_token = str(refresh)

    return access_token, refresh_token


def get_jwt_login_response(response: HttpResponse, user) -> HttpResponse:

    # Generate JWT tokens
    access_token, refresh_token = generate_jwt_tokens(user)

    # install token in cookies
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return response


def get_jwt_logout_response(
    response: HttpResponse, request: HttpRequest
) -> HttpResponse:

    # Get refresh token for cookie
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

        # Delete token in cookies
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
