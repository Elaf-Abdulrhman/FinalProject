from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('post/<int:post_id>/', views.post_details, name='post_details'),
    path('posts/', views.all_posts, name='all_posts'),
    path('add/', views.add_post, name='add_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),  # Add this line for editing posts
]
