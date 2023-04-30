from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    body = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, null=True, blank=True)


class PostImage(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/post_images')


class PostLike(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='likes')
    user_liked = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='likes')


class PostDislike(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='dislikes')
    user_disliked = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='dislikes')


class PostShare(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='sharing')
    user_shared = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sharing')
