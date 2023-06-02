from django.db import models

from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=220)


class Post(models.Model):
    body = models.TextField()
    user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="posts", null=True
    )
    category = models.ForeignKey(
        to=Category, on_delete=models.SET_NULL, related_name="posts", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, null=True, blank=True)

    class Meta:
        db_table = "posts"
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ("-created_at",)


class PostImage(models.Model):
    relation = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="media/post_images")

    class Meta:
        db_table = "post_images"
        verbose_name = "post_image"
        verbose_name_plural = "post_images"


class PostRating(models.Model):
    relation = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name="ratings"
    )
    rated_user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="post_ratings", null=True
    )
    positive = models.BooleanField(default=True)

    class Meta:
        db_table = "post_ratings"
        verbose_name = "post_rating"
        verbose_name_plural = "post_ratings"
        unique_together = [("relation", "rated_user")]


class PostSharing(models.Model):
    relation = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name="sharing"
    )
    shared_user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="post_sharing", null=True
    )

    class Meta:
        db_table = "post_sharing"
        verbose_name = "post_sharing"
        verbose_name_plural = "post_sharing"
