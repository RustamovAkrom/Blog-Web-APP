from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("user/profile/<str:username>", views.UserProfilePageView.as_view(), name="user_profile"),
    path("user/register/", views.RegisterPageView.as_view(), name="register"),
    path("user/logout/", views.LogoutView.as_view(), name="logout"),
    path("user/login/", views.LoginPageView.as_view(), name="login"),
    path("post/delete/<slug:slug>", views.PostDeleteView.as_view(), name="post_delete"),
    path("post/<slug:slug>", views.PostDetailPageView.as_view(), name="post_detail"),
    path("post/update/<slug:slug>", views.PostUpdateView.as_view(), name="post_update"),
    path("post/create/", views.PostFormPageView.as_view(), name="post_form"),
    path("post/user/", views.UserPostPageView.as_view(), name="user_posts"),
    path("post/like/<slug:slug>", views.post_like, name="post_like"),
    path("post/dislike/<slug:slug>", views.post_dislike, name="post_dislike"),
    path("post/message/<slug:slug>", views.post_message, name="post_message"),
]
