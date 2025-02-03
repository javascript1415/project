from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import User
from django.core.cache import cache
from django.db import transaction
import threading
import time

def delete_inactive_user(user_id):
    time.sleep(600)
    
    try:
        user = User.objects.get(id=user_id)
        if not user.is_active:
            time_threshold = timezone.now() - timedelta(minutes=10)
            if user.created_at <= time_threshold:
                user.delete()
    except User.DoesNotExist:
        pass

@receiver(post_save, sender=User)
def check_and_schedule_deletion(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        thread = threading.Thread(
            target=delete_inactive_user,
            args=(instance.id,)
        )
        thread.daemon = True
        thread.start()