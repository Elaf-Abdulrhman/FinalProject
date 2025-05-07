# user_notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from posts.models import Like,Post # adjust this to your actual Like model

@receiver(post_save, sender=Like)
def notify_post_like(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        liker = instance.user
        recipient = post.user

        if liker != recipient:
            notify.send(
                liker,
                recipient=recipient,
                verb='liked your post',
                target=post,
                level='info',
                description=f"{liker.username} liked your post."
            )
