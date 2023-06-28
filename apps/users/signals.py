from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (User,
                     UserProfile,)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.user_profile:
        UserProfile.objects.create()
        instance.user_profile = UserProfile.objects.latest('id')
        instance.save()