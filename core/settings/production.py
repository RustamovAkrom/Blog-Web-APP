import os

from .base import * # noqa

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "'smtp.google.com'"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DATABASES_ENVIRON = os.getenv("DATABASE_ENVIRON")

if DATABASES_ENVIRON == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": f"django.db.backends.postgresql",
            "NAME": str(os.getenv("DATABASE_NAME")),
            "USER": str(os.getenv("DATABASE_USER")),
            "PASSWORD": str(os.getenv("DATABASE_PASSWORD")),
            "HOST": str(os.getenv("DATABASE_HOST")),
            "PORT": int(os.getenv("DATABASE_PORT"))
        }
    }
elif DATABASES_ENVIRON == 'mysql':
    DATABASES = {
        "default": {
            "ENGINE": f"django.db.backends.mysql",
            "NAME": str(os.getenv("DATABASE_NAME")),
            "USER": str(os.getenv("DATABASE_USER")),
            "PASSWORD": str(os.getenv("DATABASE_PASSWORD")),
            "HOST": str(os.getenv("DATABASE_HOST")),
            "PORT": int(os.getenv("DATABASE_PORT")),
            "OPTIONS": {
                "sql_mode": "STRICT_TRANS_TABLES",
            }
        }
    }
