from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/avatars", blank=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_joined"]
