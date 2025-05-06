from django.urls import path
from . import views

app_name = 'direct_message'

urlpatterns = [
    path('', views.chat_page_view, name='chat_page_view'),
    path('<str:username>/', views.chat_page_view, name='chat_page'),
    path('edit/<int:message_id>/', views.edit_message_view, name='edit_message'),
    path('delete/<int:message_id>/', views.delete_message_view, name='delete_message'),
    path('conversation/clear/<str:username>/', views.clear_conversation, name='clear_conversation'),
]
