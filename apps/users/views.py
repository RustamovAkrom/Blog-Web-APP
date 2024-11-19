from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate

from apps.shared.mixins import CustomHtmxMixin
from apps.blog.utils import get_search_model_queryset
from apps.blog.models import Post
from .forms import RegisterForm, LoginForm
from .models import User
from .services import get_jwt_login_response, get_jwt_logout_response


class RegisterPageView(CustomHtmxMixin, View):
    template_name = "auth/register.html"

    def get(self, request):
        context = {
            "title": "Registration",
            "template_htmx": self.template_htmx,
            "form": RegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "User succesfully registered")
            response = redirect(reverse_lazy("users:login"))
            response.status_code = 302
            return response

        messages.warning(request, "Invalid registration fields!")
        response = redirect(reverse_lazy("users:register"))
        response.status_code = 400
        return response
    

class LoginPageView(CustomHtmxMixin, View):
    template_name = "auth/login.html"

    def get(self, request):
        context = {
            "title": "Login",
            "template_htmx": self.template_htmx,
            "form": LoginForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:

                response = redirect(reverse_lazy("blog:home"))

                # Login for jwt
                response = get_jwt_login_response(response, user)

                messages.success(request, f"You are logged in as { username }")
                return response

            messages.error(request, "Invalid username or password.")

        return redirect(reverse_lazy("users:login"))
        

class LogoutPageView(CustomHtmxMixin, LoginRequiredMixin, View):
    template_name = "auth/logout.html"

    def get(self, request):
        context = {
            "title": "Logout",
            "template_htmx": self.template_htmx
        }
        return render(request, self.template_name, context)

    def post(self, request):
        response = redirect(reverse("blog:home"))

        # Logout and remove jwt (refresh, access) tokens
        response = get_jwt_logout_response(response, request)

        return response


class UserProfilePageView(CustomHtmxMixin, View):
    template_name = "blog/profile.html"

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.published.filter(author=user).all().order_by("-created_at")

        search_query = request.GET.get("search_query_for_user_profile", None)

        if search_query is not None:
            posts = get_search_model_queryset(posts, search_query)

        context = {
            "title": str(user),
            "template_htmx": self.template_htmx,
            "posts": posts, 
            "user": user
        }
        return render(request, self.template_name, context)
