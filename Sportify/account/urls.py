from django.urls import path
from . import views

app_name="account"

urlpatterns = [
    
    path("signup/", views.sign_up_as_view,name="sign_up_as_view"),
    path("signup/as/athlete/", views.signup_athlete_view, name="signup_athlete_view"),
    path("signup/as/club/", views.signup_club_view, name="signup_club_view"),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
]

