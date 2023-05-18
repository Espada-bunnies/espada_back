import pytest

from apps.posts.models import Post
from apps.users.models import User


@pytest.fixture
def create_users(api_client):
    User.objects.create(username="Xelo", password="23123Jdasdwe", email="nano@mail.ru")
    User.objects.create(
        username="Ceas", password="(9kddkJJJ", email="yamulfile@mail.ru"
    )
    User.objects.create(
        username="Roma", password="_-ddsJJJd22", email="sobaka@gmail.com"
    )


@pytest.fixture
def create_posts(api_client):
    Post.objects.create(body="Лошата ми контаре", user_id=2)
    Post.objects.create(body="Асталависта бейби", user_id=3)
    Post.objects.create(body="Ал би бэк", user_id=1)


@pytest.fixture
def headers(api_client):
    data = {
        "username": "omgsheet",
        "email": "nanotaro@mail.ru",
        "password": "189212Jajo-",
        "confirm_password": "189212Jajo-"
    }
    response = api_client.post(path="/api/v1/users/register/", data=data)
    token = response.data.get("access_token")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return headers
