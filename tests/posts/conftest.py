import pytest
from apps.users.models import User

from apps.posts.models import Post


@pytest.fixture
def create_users(api_client):
    User.objects.create(username="Xelo", password="23123Jdasdwe", email='nano@mail.ru')
    User.objects.create(username="Ceas", password="(9kddkJJJ", email='yamulfile@mail.ru')
    User.objects.create(username="Roma", password="_-ddsJJJd22", email='sobaka@gmail.com')


@pytest.fixture
def create_posts(api_client):
    Post.objects.create(body="Лошата ми контаре", user_id=2)
    Post.objects.create(body="Асталависта бейби", user_id=3)
    Post.objects.create(body="Ал би бэк", user_id=1)
