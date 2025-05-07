# user_notifications/urls.py
from django.urls import path
from . import views

app_name = 'user_notifications'

urlpatterns = [
    path('', views.inbox, name='inbox'),
]
