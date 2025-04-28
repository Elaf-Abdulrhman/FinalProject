from django.urls import path
from . import views

app_name = 'bookmarks'  # Define the namespace

urlpatterns = [
    path('bookmark_post/<int:post_id>/', views.bookmark_post, name='bookmark_post'),
    path('all_bookmarks/', views.all_bookmarks, name='all_bookmarks'),
]