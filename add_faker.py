from faker import Faker
import datetime
import random
from faker.providers.company import Provider

def CreateUser():
    fake = Faker()
    user = User.objects.create(
        username = fake.user_name(),
        first_name = fake.first_name(),
        last_name = fake.last_name(),
        password = fake.password(),
        email = fake.email()
    )
    user.save()
    return user


def CreatePost(user):
    fake = Faker()
    post = Post.objects.create(
        title = str(Provider(fake).company()),
        content = fake.text(),
        publisher_at = datetime.datetime.now().strftime('%Y-%m-%d'),
        is_active = True,
        author = user
    )
    post.save()


def main():
    for _ in range(10):
        user = CreateUser()
        CreatePost(user)




if __name__=='__main__':
    import os

    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    application = get_wsgi_application()

    from blog.models import User, Post

    main()
