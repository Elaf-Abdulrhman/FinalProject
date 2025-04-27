# subscriptions/models.py
from django.db import models

class Payment(models.Model):
    payment_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()  # in halalas
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
