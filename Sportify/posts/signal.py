# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like
from user_notifications.models import Notification
from django.contrib.auth.models import User

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        post_owner = instance.post.user
        liker = instance.user

        if post_owner != liker:
            message = f"{liker.username} liked your post: {instance.post.content}"
            
            # Prevent duplicate notification
            if not Notification.objects.filter(recipient=post_owner, message=message).exists():
                Notification.objects.create(
                    recipient=post_owner,
                    message=message
                )

