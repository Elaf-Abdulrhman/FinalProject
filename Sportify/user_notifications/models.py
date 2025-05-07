from django.db import models
from django.contrib.auth.models import User

class NotificationQuerySet(models.QuerySet):
    def unread(self):
        return self.filter(read=False)

    def mark_all_as_read(self):
        return self.update(read=True)

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='notifications_user_notifications')
    message = models.TextField(default="No message")
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Add this field
    
    
    objects = NotificationQuerySet.as_manager()

    def __str__(self):
        return self.message
