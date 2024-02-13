from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(),                                        name='home'),
    path('About-page/', AboutPageView.as_view(),                            name='about'),
    path('Profile-page/',UserProfilePageView.as_view(),                     name='profile'),
    path('Register-page/',RegisterPageView.as_view(),                       name='register'),
    path('Logout-page', LogoutView.as_view(),                               name='logout'),
    path('Login-page/', LoginPageView.as_view(),                            name='login'),
    path('Post-confirm-Delete-Page/<int:id>', post_delete,                  name='post_delete'),
    path('Post-Detail-page/<int:id>', PostDetailPageView.as_view(),         name='post_detail'),
    path('Post-Update-page/<int:id>', post_update,                          name='post_update'),
    path('Post-Form-page/', PostFormPageView.as_view(),                     name='post_form'),
    path('User-Posts/', UserPostPageView.as_view(),                         name='user_posts'),
]
