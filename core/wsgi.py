import os

from dotenv import load_dotenv
load_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv(
    "DJANGO_SETTINGS_MODULE", "core.settings.development"
))

application = get_wsgi_application()

app = application
