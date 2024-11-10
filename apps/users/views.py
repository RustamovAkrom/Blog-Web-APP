from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout, login, authenticate
from .forms import RegisterForm, LoginForm
from .models import User
from apps.blog.utils import get_search_model_queryset
from apps.blog.models import Post

from rest_framework_simplejwt.tokens import RefreshToken


class RegisterPageView(View):
    template_name = "auth/register.html"

    def get(self, request):
        return render(request, "auth/register.html", {"form": RegisterForm()})

    def post(self, request):

        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "User succesfully registered")
            return redirect(reverse("users:login"))

        messages.warning(request, "Error registered!")
        return render(request, "auth/register.html", {"form": form})


class LoginPageView(View):
    template_name = "auth/login.html"

    def get(self, request):
        return render(request, "auth/login.html", {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                # login(request, user)

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # install token in cookies
                response = redirect(reverse("blog:home"))
                response.set_cookie("access_token", access_token, httponly=True)
                response.set_cookie("refresh_token", refresh_token, httponly=True)
                
                messages.info(request, f"You are logged in as { username }")
                return response

            else:
                messages.error(request, "Invalid username or password.")
                return redirect(reverse("users:login"))

        return render(request, "auth/login.html", {"form": form})


class LogoutPageView(LoginRequiredMixin, View):
    template_name = "auth/logout.html"

    def get(self, request):
        return render(request, "auth/logout.html")

    def post(self, request):
        # logout(request)
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = redirect(reverse("blog:home"))
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


class UserProfilePageView(View):
    template_name = "blog/profile.html"

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=user, is_active=True).all().order_by("id")

        search_query = request.GET.get("search_query_for_user_profile", None)

        if search_query is not None:
            posts = get_search_model_queryset(posts, search_query)

        return render(request, "blog/profile.html", {"posts": posts, "user": user})
