from django.urls import path
from . import views

app_name = 'direct_message'

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox_view'),
    path('<str:username>/', views.direct_chat_view, name='direct_chat_view'),
]
