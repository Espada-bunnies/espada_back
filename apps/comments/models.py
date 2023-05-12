from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from apps.posts.models import Post


class Comment(MPTTModel):
    post = models.ForeignKey(to=Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(
        to=User, related_name="comments", on_delete=models.SET_NULL, null=True
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.BooleanField(default=False, editable=False)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        db_table = "comments"
        verbose_name = "comment"
        verbose_name_plural = "comments"
        order_insertion_by = ("-created_at",)

    def __str__(self):
        return f"{self.body[:20]}..."


class CommentImage(models.Model):
    relation = models.ForeignKey(
        to=Comment, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="media/comment_images")


class CommentRating(models.Model):
    relation = models.ForeignKey(
        to=Comment, on_delete=models.CASCADE, related_name="ratings"
    )
    rated_user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="comment_ratings", null=True
    )
    positive = models.BooleanField(default=True)

    class Meta:
        db_table = "comment_ratings"
        verbose_name = "comment_rating"
        verbose_name_plural = "comment_ratings"
        unique_together = [("relation", "rated_user")]


class CommentSharing(models.Model):
    relation = models.ForeignKey(
        to=Comment, on_delete=models.CASCADE, related_name="sharing"
    )
    shared_user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="comment_sharing", null=True
    )

    class Meta:
        db_table = "comment_sharing"
        verbose_name = "comment_sharing"
        verbose_name_plural = "comment_sharing"
