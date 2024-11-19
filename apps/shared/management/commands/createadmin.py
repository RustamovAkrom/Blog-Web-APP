import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from dotenv import load_dotenv
load_dotenv()


ADMIN_USERNAME = str(os.getenv("ADMIN_USERNAME"))
ADMIN_PASSWORD = str(os.getenv("ADMIN_PASSWORD"))
ADMIN_EMAIL = str(os.getenv("ADMIN_PASSWORD"))


class Command(BaseCommand):
    help = "Create superuser"

    def handle(self, *args, **options):
        User = get_user_model()
        self.create_superuser(User, ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)

    def create_superuser(self, User, username, email, password):
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} created successfully.")
            )
        else:
            self.stdout.write(self.style.ERROR(f"Superuser {username} already exists."))
