from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from comments.models import Comment
from posts.models import Post
from http import HTTPStatus


class CommentTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'body': 'Тестовые данные',
        }

        self.user1 = User.objects.create(username='Indigo', password='12312Kaki')

        self.post1 = Post.objects.create(body='Шарлатаны мимо', user=self.user1)
        self.comment1 = Comment.objects.create(body='По ресторанам', user=self.user1, post=self.post1)
        self.comment2 = Comment.objects.create(body='Да я тут', user=self.user1, post=self.post1)

        self.post2 = Post.objects.create(body='Замкнутыми стенами давила та печаль', user=self.user1)

    def test_get_list(self):
        response = self.client.get('http://127.0.0.1:8000/posts/1/comments/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(len(response.data) == 2)
        self.assertIsInstance(response.data, list)

        response2 = self.client.get('http://127.0.0.1:8000/posts/2/comments/')
        self.assertEqual(response2.status_code, HTTPStatus.OK)
        self.assertTrue(response2.data == [])
        self.assertIsInstance(response2.data, list)

    def test_get_detail(self):
        response1 = self.client.get('http://127.0.0.1:8000/posts/1/comments/1/')
        self.assertEqual(response1.status_code, HTTPStatus.OK)
        self.assertEqual(response1.data['id'], self.comment1.id)
        self.assertIsInstance(response1.data, dict)

        response2 = self.client.get('http://127.0.0.1:8000/posts/2/comments/1/')
        self.assertEqual(response2.status_code, HTTPStatus.NOT_FOUND)

    def test_create(self):
        response = self.client.post(
            'http://127.0.0.1:8000/posts/2/comments/',
            data=self.data,
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_partial_update(self):
        resp = self.client.post(
            'http://127.0.0.1:8000/posts/2/comments/',
            data=self.data,
        )
        resp2 = self.client.patch(
            f"http://127.0.0.1:8000/posts/2/comments/{resp.data['id']}/",
            data={
                'body': 'Это тест'
            }
        )
        self.assertEqual(resp2.status_code, HTTPStatus.OK)
        response = self.client.get(f"http://127.0.0.1:8000/posts/2/comments/{resp2.data['id']}/")
        self.assertEqual(response.data['body'], 'Это тест')

    def test_delete(self):
        response = self.client.delete('http://127.0.0.1:8000/posts/1/comments/1/')
        self.assertEqual(response.status_code, 204)