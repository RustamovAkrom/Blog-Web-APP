import os

from pathlib import Path

from django.utils.translation import gettext_lazy

from core.config import *  # noqa

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = str(os.getenv("SECRET_KEY"))

DEBUG = bool(os.getenv("DEBUG", True))

ALLOWED_HOSTS = str(os.getenv("ALLOWED_HOSTS")).split(",")

# CSRF_TRUSTED_ORIGINS = str(os.getenv("CSRF_TRUSTED_ORIGINS")).split(",")

INSTALLED_APPS = THIRD_PARTY_APPS + DEFAULT_APPS + PROJECT_APPS  # noqa


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.users.middleware.JWTAuthMiddleware",  # My Jwt Auth Middleware
]

ROOT_URLCONF = "core.urls"


TEMPLATES_DIRS = [BASE_DIR.joinpath("templates")]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATES_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.joinpath("db.sqlite3"),
    },
}

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

gettext = lambda s: gettext_lazy(s) # noqa

LANGUAGES = (
    ("ru", gettext("Russia")),
    ("en", gettext("English")),
    ("uz", gettext("Uzbek")),
)

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"

STATIC_URL = "static/"
STATICFILES_DIRS = [str(BASE_DIR.joinpath("static"))]
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))

# AUTHENTICATION_BACKENDS = (
#     'apps.users.authentication.JWTAdminAuthentication',
#     'django.contrib.auth.backends.ModelBackend',
# )

MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.joinpath("media/"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

SITE_ID = 1

DEFAULT_FILE_STORAGE = "django.core/files.storage.FileSystemStorage"
