import os

from .base import * # noqa

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "'smtp.google.com'"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{str(os.getenv('DATABASE_ENVIRON'))}",
        "NAME": str(os.getenv("DATABASE_NAME")),
        "USER": str(os.getenv("DATABASE_USER")),
        "PASSWORD": str(os.getenv("DATABASE_PASSWORD")),
        "HOST": str(os.getenv("DATABASE_HOST")),
        "PORT": int(os.getenv("DATABASE_PORT"))
    }
}

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": os.getenv("REDIS_CACHE_URL"),
#     },
# }
