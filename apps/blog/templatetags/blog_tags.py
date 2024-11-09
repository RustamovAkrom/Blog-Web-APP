from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from ..models import Post, PostLike, PostDislike

import markdown2

register = template.Library()

@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown2.markdown(text))


@register.filter(name="check_like")
def check_like(post, user) -> bool:
    return PostLike.objects.filter(post=post, user=user).exists()


@register.filter(name="check_dislike")
def check_dislike(post, user) -> bool:
    return PostDislike.objects.filter(post=post, user=user).exists()
