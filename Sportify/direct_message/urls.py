from django.urls import path
from . import views

app_name = 'direct_message'

urlpatterns = [
    path('', views.chat_page_view, name='chat_page_view'),
    path('<str:username>/', views.chat_page_view, name='chat_page'),
]
