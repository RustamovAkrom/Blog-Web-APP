from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


app_name = "users"

urlpatterns = [
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("register/", views.RegisterPageView.as_view(), name="register"),
    path("logout/", views.LogoutPageView.as_view(), name="logout"),
    path(
        "profile/<str:username>",
        views.UserProfilePageView.as_view(),
        name="user_profile",
    ),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
