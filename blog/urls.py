from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('profile/',UserProfilePageView.as_view(), name='profile'),
    path('register/',RegisterPageView.as_view(),name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('post/delete/<int:id>', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:id>', PostDetailPageView.as_view(), name='post_detail'),
    path('Post/update/<int:id>', PostUpdateView.as_view(), name='post_update'),
    path('post/create/', PostFormPageView.as_view(), name='post_form'),
    path('post/user/', UserPostPageView.as_view(), name='user_posts'),
]
