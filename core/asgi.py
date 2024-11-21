import os

from django.core.asgi import get_asgi_application

from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", 
    os.getenv("DJANGO_SETTINGS_MODULE", "core.settings.development")
)

application = get_asgi_application()

app = application