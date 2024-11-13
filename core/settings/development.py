from .base import * # noqa

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}