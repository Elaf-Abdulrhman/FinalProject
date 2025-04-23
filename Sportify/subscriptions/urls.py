from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('plus/', views.plus_plan, name='plus_plan'),
    path('payment/', views.payment, name='payment'),
]
