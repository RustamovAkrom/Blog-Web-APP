import os

from .base import * # noqa

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{str(os.getenv('DATABASE_ENVIRON'))}",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}