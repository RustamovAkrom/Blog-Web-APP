from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from ..models import Post

import markdown2

register = template.Library()

@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown2.markdown(text))
