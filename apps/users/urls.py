from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("user/login/", views.LoginPageView.as_view(), name="login"),
    path("user/register/", views.RegisterPageView.as_view(), name="register"),
    path("user/logout/", views.LogoutPageView.as_view(), name="logout"),
]
