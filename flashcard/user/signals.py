from django.db.models.signals import pre_save
import os
from django.dispatch import receiver
from .models import LearnerUser

@receiver(pre_save, sender=LearnerUser)
def delete_old_avatar(sender, instance, **kwargs):
    # on creation, signal callback won't be triggered 
    if instance._state.adding and not instance.pk:
        return False
    
    try:
        old_avatar = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    
    # comparing the new file with the old one
    avatar = instance.avatar
    if not old_avatar == avatar:
        if os.path.isfile(old_avatar.path):
            print("da xoa avatar cu")
            os.remove(old_avatar.path)