from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class City(models.Model):
    city_name= models.CharField(max_length=50)
    

    
    
class Sport(models.Model):
    sport_name=models.CharField(max_length=25)
    

   
