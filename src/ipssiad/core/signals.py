from django.db import models
from django.dispatch import receiver

from .models import Profile
from .utils import delete_file


@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_filesystem(sender, instance, **kwargs):
    if instance.avatar:
        delete_file(instance.avatar.path)
