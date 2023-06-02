import logging
from http import HTTPStatus

import pytest

logger = logging.getLogger("django")

pytestmark = pytest.mark.django_db


class TestPostEndpoint:
    endpoint = "/api/v1/posts/"

    def test_get_all(self, api_client, create_users, create_posts):
        response = api_client.get(self.endpoint)
        assert response.status_code == HTTPStatus.OK
        assert len(response.data) == 3

    def test_get_one(self, api_client, create_users, create_posts):
        response = api_client.get(f"{self.endpoint}2/")
        assert response.status_code == HTTPStatus.OK
        assert response.data["id"] == 2

        response_2 = api_client.get(f"{self.endpoint}4/")
        assert response_2.status_code == HTTPStatus.NOT_FOUND

    def test_create(self, api_client, create_users, headers):
        data = {
            "body": "Всем привет",
            "user_id": 3,
        }
        response = api_client.post(self.endpoint, data, headers=headers)
        assert response.status_code == HTTPStatus.CREATED

    def test_create_validator(self, api_client, create_users, headers):
        data = {
            "body": "На сука, я это сделал",
            "user_id": 2,
        }
        response = api_client.post(self.endpoint, data, headers=headers)
        assert response.status_code == 400
        assert response.data["body"][0] == "Текст содержит нецензурные слова"

        data_2 = {
            "body": "Это текст без матов",
            "user_id": 2,
            "upload_images": ["image" for _ in range(6)],
        }
        response_2 = api_client.post(self.endpoint, data_2, headers=headers)
        assert response_2.status_code == 400
