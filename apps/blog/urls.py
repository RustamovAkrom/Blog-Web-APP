from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("profile/", views.UserProfilePageView.as_view(), name="profile"),
    path("register/", views.RegisterPageView.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("post/delete/<int:id>", views.PostDeleteView.as_view(), name="post_delete"),
    path("post/<int:id>", views.PostDetailPageView.as_view(), name="post_detail"),
    path("Post/update/<int:id>", views.PostUpdateView.as_view(), name="post_update"),
    path("post/create/", views.PostFormPageView.as_view(), name="post_form"),
    path("post/user/", views.UserPostPageView.as_view(), name="user_posts"),
]
