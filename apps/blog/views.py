import datetime
from functools import wraps
from typing import Any

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView
from django.contrib import messages
from django.http import HttpRequest
from django.views import View
from django.urls import reverse

from apps.users.models import User
from apps.shared.mixins import CustomHtmxMixin, render_htmx_or_default
from .models import Post
from .forms import (
    PostCreateUpdateForm,
    SettingsUserForm,
    SettingsUserProfileForm,
)
from .utils import (
    get_search_model_queryset,
    get_pagination_obj,
    set_post_like,
    set_post_dislike,
    set_post_comment,
)


class HomePageView(CustomHtmxMixin, TemplateView):
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        if self.request.user is not None and self.request.user.is_authenticated:
            posts = Post.published.exclude(author=self.request.user)
        else:
            posts = Post.published.all()

        search_query = self.request.GET.get("search_query", None)
        page = self.request.GET.get("page", 1)
        size = self.request.GET.get("size", 4)

        posts = get_search_model_queryset(posts, search_query)

        page_obj = get_pagination_obj(posts, page, size)

        kwargs["title"] = "Home"
        kwargs["page_obj"] = page_obj
        kwargs["size_value"] = size
        kwargs["search_query_value"] = search_query

        return super().get_context_data(**kwargs)


class AboutPageView(CustomHtmxMixin, TemplateView):
    template_name = "blog/about.html"
    
    def get_context_data(self, **kwargs):
        kwargs["title"] = "About"
        return super().get_context_data(**kwargs)


class ContactsPageView(CustomHtmxMixin, TemplateView):
    template_name = "blog/contacts.html"

    def get_context_data(self, **kwargs):
        kwargs["title"] = "Contacts"
        return super().get_context_data(**kwargs)


class PostDetailPageView(CustomHtmxMixin, View):
    template_name = "blog/post_detail.html"

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        
        post_comments = post.post_comments.all().order_by("-created_at")
        post.watching += 1
        post.save()

        context = {
            "title": post.title,
            "post": post, 
            "post_comments": post_comments,
            "template_htmx": self.template_htmx
        }

        return render(request, self.template_name, context)


class PostCreatePageView(CustomHtmxMixin, LoginRequiredMixin, TemplateView):
    template_name = "blog/post_create.html"

    def get_context_data(self, **kwargs):
        kwargs["form"] = PostCreateUpdateForm()
        kwargs["title"] = "Post Create"
        return super().get_context_data(**kwargs)
    # def get(self, request):
    #     return render(request, self.template_name, {"form": PostCreateUpdateForm()})

    def post(self, request):
        form = PostCreateUpdateForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post = Post.objects.create(
                title=cd.get("title"),
                status=cd.get("status"),
                description=cd.get("description"),
                content=cd.get("content"),
                author=request.user,
                publisher_at=datetime.datetime.now().strftime("%Y-%m-%d"),
            )
            post.save()

            messages.success(request, "Post succesfully created")
            return redirect("blog:home")

        messages.warning(
            request,
            "There is a mistake in your post ! or your post is not filled to the depth.",
        )
        return redirect(reverse("blog:post_create"))


class PostUpdateView(CustomHtmxMixin, LoginRequiredMixin, TemplateView):
    template_name = "blog/post_update.html"

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, is_active=True)
        
        form = PostCreateUpdateForm(instance=post)
        context = {
            "title": "Update " + post.title,
            "template_htmx": self.template_htmx,
            "form": form, 
            "post": post
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = PostCreateUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post succsessfully updated")
            return redirect(reverse("blog:post_update", kwargs={"slug": slug}))

        messages.error(request, "You`r post is not valid !")
        return redirect(reverse("blog:post_update", kwargs={"slug": slug}))


class UserPostsPageView(CustomHtmxMixin, LoginRequiredMixin, TemplateView):
    template_name = "blog/user_posts.html"

    def get(self, request):

        search_query_for_user_posts = request.GET.get(
            "search_query_for_user_posts", None
        )
        posts = Post.objects.filter(author=request.user, is_active=True)

        if search_query_for_user_posts is not None:
            posts = get_search_model_queryset(posts, search_query_for_user_posts)

        context = {
            "title": "My posts",
            "template_htmx": self.template_htmx,
            "posts": posts.order_by("-created_at")
        }
        return render(request, self.template_name, context)


class PostDeletePageView(CustomHtmxMixin, LoginRequiredMixin, DeleteView):
    template_name = "blog/post_confirm_delete.html"
    model = Post

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        messages.success(request, "post successfully deleted")
        return redirect("blog:user_posts")


class SettingsPageView(CustomHtmxMixin, LoginRequiredMixin, View):
    template_name = "blog/settings.html"

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = SettingsUserForm(instance=user)
        user_profile_form = SettingsUserProfileForm(instance=user.profiles)
        context = {
            "title": "Settings",
            "template_htmx": self.template_htmx,
            "user_form": user_form, 
            "user_profile_form": user_profile_form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = SettingsUserForm(data=request.POST, instance=user)
        user_profile_form = SettingsUserProfileForm(
            data=request.POST, files=request.FILES, instance=user.profiles
        )
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()

            messages.success(request, "Successfully updated profile settings.")
            return redirect(reverse("blog:user_settings"))

        messages.error(request, "Invalid parametres.")
        return redirect(reverse("blog:user_settings"))


def post_like(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login"))
    set_post_like(request.user, slug)
    return redirect(reverse("blog:post_detail", kwargs={"slug": slug}))


def post_dislike(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login"))
    set_post_dislike(request.user, slug)
    return redirect(reverse("blog:post_detail", kwargs={"slug": slug}))


def post_message(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login"))

    post_message_input = request.GET.get("post_message_input", None)

    if post_message_input is not None:
        set_post_comment(request.user, slug, post_message_input)
    return redirect(reverse("blog:post_detail", kwargs={"slug": slug}))
