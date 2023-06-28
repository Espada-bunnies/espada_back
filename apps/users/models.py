from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(models.Model):

    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    interests = models.TextField(blank=True)



class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/avatars", blank=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    user_profile = models.OneToOneField(UserProfile,on_delete=models.CASCADE,null=True)

    class Meta:
        ordering = ["-date_joined"]



