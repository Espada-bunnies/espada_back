from django.contrib.auth.models import User
from django.db import models

from posts.models import Post


class Comment(models.Model):
    post = models.ForeignKey(to=Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.BooleanField(default=False, editable=False)

    class Meta:
        db_table = 'comments'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return f'{self.body[:20]}...'


class CommentReply(models.Model):
    comment = models.OneToOneField(to=Comment, on_delete=models.CASCADE, primary_key=True)
    reply_to = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='replies')


class CommentImage(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/comment_images')


class CommentLike(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='likes')
    user_liking = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('comment', 'user_liking')
        ]


class CommentDislike(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name='dislikes')
    user_disliking = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('comment', 'user_disliking')
        ]
