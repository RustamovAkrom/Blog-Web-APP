from django.db.models import QuerySet
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import (
    Paginator,
    Page,
    EmptyPage,
    PageNotAnInteger,
    InvalidPage,
)
from django.conf import settings

from .models import PostLike, PostDislike, Post, PostComment


def get_search_model_queryset(model_queryset: QuerySet, query: str = None) -> QuerySet:
    if not query:
        return model_queryset

    search_vector = SearchVector("title", "description", "content")
    search_query = SearchQuery(query)

    if settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
        # PostgreSQL search
        queryset = (
            model_queryset.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query),
            )
            .filter(search=search_query)
            .order_by("-rank")
        )
    else:
        # SQLite3 search
        queryset = model_queryset.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(content__icontains=query)
        )

    return queryset


def get_pagination_obj(model_queryset: QuerySet, page: int = 1, size: int = 4) -> Page:
    paginator = Paginator(model_queryset.order_by("-created_at"), size)

    try:
        page_obj = paginator.page(page)

    except PageNotAnInteger:
        page_obj = paginator.page(1)

    except InvalidPage:
        page_obj = paginator.page(1)

    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj


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
