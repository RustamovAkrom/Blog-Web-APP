from django.db.models import TextChoices


class StatusChoice(TextChoices):
    DRAFT = 'df', 'Draft'
    PUBLISHED = 'pb', 'Published'
