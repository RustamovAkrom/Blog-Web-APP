import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.views import View
from django.urls import reverse

from .forms import RegisterForm, LoginForm, PostUpdateForm, PostCreateForm
from .models import Post, PostComment
from .utils import (
    get_search_model_queryset, 
    get_pagination_obj, 
    set_post_like, 
    set_post_dislike, 
    set_post_comment
)


class CustomHtmxMixin:
    def dispatch(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        self.template_htmx = self.template_name
        if not self.request.META.get("HTTP_HX_REQUEST"):
            self.template_name = "blog/include_blog.html"
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs["template_htmx"] = self.template_htmx
        return super().get_context_data(**kwargs)


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


class LogoutView(View):
    template_name = "auth/logout.html"

    def get(self, request):
        return render(request, "auth/logout.html")

    def post(self, request):
        logout(request)
        return redirect("home")


class HomePageView(TemplateView):
    template_name = "blog/home.html"

    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.exclude(author=request.user)
        else:
            posts = Post.objects.all()

        search_query = request.GET.get('search_query', None)
        page = request.GET.get("page", 1)
        size = request.GET.get("size", 4)
        
        posts = get_search_model_queryset(posts, search_query)

        page_obj = get_pagination_obj(posts, page, size)

        return render(
            request,
            "blog/home.html",
            {
                "page_obj": page_obj,
                "size_value": size,
            },
        )


class AboutPageView(TemplateView):
    template_name = "blog/about.html"


class PostDetailPageView(View):
    template_name = "blog/post_detail.html"

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post_comments = post.post_comments.all().order_by("-created_at")
        post.watching += 1
        post.save()
        return render(
            request, 
            "blog/post_detail.html", 
            {
                "post": post,
                "post_comments": post_comments
            }
        )


class UserProfilePageView(LoginRequiredMixin, View):
    template_name = "blog/user_posts.html"

    def get(self, request):
        posts = Post.objects.filter(author=request.user)
        return render(request, "blog/user_posts.html", {"posts": posts})


class PostFormPageView(LoginRequiredMixin, TemplateView):
    template_name = "blog/post_form.html"

    def get(self, request):
        return render(request, "blog/post_form.html", {"form": PostCreateForm()})

    def post(self, request):
        form = PostCreateForm(request.POST)

        if form.is_valid():

            post = Post.objects.create(
                title=form.cleaned_data.get("title"),
                content=form.cleaned_data.get("content"),
                is_active=form.cleaned_data.get("is_active"),
                author=request.user,
                publisher_at=datetime.datetime.now().strftime("%Y-%m-%d"),
            )
            post.save()

            messages.success(request, "Post succesfully created")
            return redirect("home")
        messages.warning(
            request,
            "There is a mistake in your post ! or your post is not filled to the depth.",
        )
        return render(request, "blog/post_form.html", {"form": form})


class UserPostPageView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"


class PostUpdateView(LoginRequiredMixin, View):
    template_name = "blog/post_update.html"

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = PostUpdateForm(instance=post)
        return render(request, "blog/post_update.html", {"form": form, "post": post})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            messages.success(request, "Post succsessfully updated")
            form.save()
            return redirect("profile")

        messages.error(request, "You`r post is not valid !")
        return render(request, "blog/post_update.html", {"form": form})


class PostDeleteView(LoginRequiredMixin, View):
    template_name = "blog/post_confirm_delete.html"

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post_messages = post.post_comments.all()
        print(post_messages)
        return render(
            request, 
            "blog/post_confirm_delete.html", 
            {
                "post": post, "post_messages": post_messages
            }
        )

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        messages.success(request, "post successfully deleted")
        post.delete()
        return redirect("profile")


class ContactsView(TemplateView):
    template_name = "blog/contacts.html"


def post_like(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    set_post_like(request.user, slug)
    return redirect(reverse("post_detail", kwargs={"slug": slug}))


def post_dislike(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    set_post_dislike(request.user, slug)
    return redirect(reverse("post_detail", kwargs={"slug": slug}))


def post_message(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    
    post_message_input = request.GET.get("post_message_input", None)
    print(post_message_input)

    if post_message_input is not None:
        set_post_comment(request.user, slug, post_message_input)
    return redirect(reverse("post_detail", kwargs={"slug": slug}))
