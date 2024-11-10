from django.urls import path
from . import views


app_name = "blog"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts"),
    path("delete/<slug:slug>", views.PostDeletePageView.as_view(), name="post_delete"),
    path("<slug:slug>", views.PostDetailPageView.as_view(), name="post_detail"),
    path("update/<slug:slug>", views.PostUpdateView.as_view(), name="post_update"),
    path("create/", views.PostCreatePageView.as_view(), name="post_create"),
    path("user/", views.UserPostsPageView.as_view(), name="user_posts"),
    path("like/<slug:slug>", views.post_like, name="post_like"),
    path("post/dislike/<slug:slug>", views.post_dislike, name="post_dislike"),
    path("post/message/<slug:slug>", views.post_message, name="post_message"),
]
