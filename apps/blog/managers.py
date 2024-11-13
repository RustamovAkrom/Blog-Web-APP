from django.db import models
from .choices import StatusChoice


class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return (
            super().get_queryset().filter(status=StatusChoice.PUBLISHED, is_active=True)
        )
