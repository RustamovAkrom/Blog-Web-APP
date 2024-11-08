from django.db.models import QuerySet
from django.core.paginator import Paginator, Page


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
