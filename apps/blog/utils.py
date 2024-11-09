from django.db.models import QuerySet
from django.core.paginator import Paginator, Page
from django.shortcuts import redirect
from django.urls import reverse

from .models import PostLike, PostDislike, Post, PostComment


def get_search_model_queryset(model_queryset: QuerySet, search_query: str = None) -> QuerySet:
    if search_query is None:
        return model_queryset

    search_for_title = model_queryset.filter(title__icontains=search_query)
    if not search_for_title:
        search_for_content = model_queryset.filter(content__icontains=search_query)
        if not search_for_content:
            search_for_publisher_at = model_queryset.filter(publisher_at__icontains=search_query)
            queryset = search_for_publisher_at
        else:
            queryset = search_for_content
    else:
        queryset = search_for_title
    return queryset


def get_pagination_obj(model_queryset: QuerySet, page: int = 1, size: int = 4) -> Page:
    return Paginator(model_queryset.order_by("id"), size).page(page)


def set_post_like(user, slug) -> None:
    post = Post.objects.get(slug=slug)

    get_post_dislike = PostDislike.objects.filter(user=user, post=post)
    if get_post_dislike.exists():
        get_post_dislike.first().delete()

    like, created = PostLike.objects.get_or_create(user=user, post=post)
    if not created:
        like.delete()


def set_post_dislike(user, slug) -> None:
    post = Post.objects.get(slug=slug)

    get_post_like = PostLike.objects.filter(user=user, post=post)
    if get_post_like.exists():
        get_post_like.first().delete()

    dislike, created = PostDislike.objects.get_or_create(user=user, post=post)
    if not created:
        dislike.delete()


def set_post_comment(user, slug, message: str) -> None:
    post = Post.objects.get(slug=slug)
    PostComment.objects.create(post=post, user=user, message=message)
