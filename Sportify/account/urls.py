from django.urls import path
from . import views

app_name="account"

urlpatterns = [
    
    path("signup/", views.sign_up_as_view,name="sign_up_as_view"),
    path("profile/", views.profile_view,name="profile_view"),
]

