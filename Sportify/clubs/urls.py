from django.urls import path
from . import views

app_name = 'clubs'
urlpatterns = [
    path('all/', views.all_clubs, name='all_clubs'),
    path('club_dashboard/', views.club_dashboard, name='club_dashboard'),
]
