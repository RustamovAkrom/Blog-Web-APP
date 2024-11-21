DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

PROJECT_APPS = [
    "apps.shared.apps.SharedConfig",
    "apps.blog.apps.BlogConfig",
    "apps.users.apps.UsersConfig",
]

THIRD_PARTY_APPS = [
    # Admin panel
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    # Translation
    "modeltranslation",
    #
    "django_ckeditor_5",
    # Translation pannel
    "rosetta",
    # DRF Swaggers
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # Rest Framework
    "rest_framework",
    # Rest Framework JWT (Json web token)s
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]
