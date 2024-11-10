from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout, login, authenticate
from .forms import RegisterForm, LoginForm
from .models import User
from apps.blog.utils import get_search_model_queryset
from apps.blog.models import Post


class RegisterPageView(View):
    template_name = "auth/register.html"

    def get(self, request):
        return render(request, "auth/register.html", {"form": RegisterForm()})

    def post(self, request):

        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "User succesfully registered")
            return redirect("login")
        else:
            messages.warning(request, "Error registered!")
            return render(request, "blog/register.html", {"form": form})


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
                login(request, user)
                messages.info(request, f"You are logged in as { username }")
                return redirect("home")

            else:
                messages.error(request, "Invalid username or password.")
                return redirect("login")

        return render(request, "auth/login.html", {"form": form})


class LogoutPageView(LoginRequiredMixin, View):
    template_name = "auth/logout.html"

    def get(self, request):
        return render(request, "auth/logout.html")

    def post(self, request):
        logout(request)
        return redirect("home")


class UserProfilePageView(View):
    template_name = "blog/profile.html"

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=user, is_active=True).all().order_by("id")

        search_query = request.GET.get("search_query_for_user_profile", None)
        
        if search_query is not None:
            posts = get_search_model_queryset(posts, search_query)
    
        return render(
            request, 
            "blog/profile.html", 
            {
                "posts": posts,
                "user": user
            }
        )
