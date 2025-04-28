# subscriptions/models.py
from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status} ({self.user.username})"