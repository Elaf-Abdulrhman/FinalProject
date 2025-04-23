from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Athlete, Club

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class ClubUserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AthleteSignupForm(forms.ModelForm):
    class Meta:
        model = Athlete
        exclude = ['user']

class ClubSignupForm(forms.ModelForm):
    class Meta:
        model = Club
        exclude = ['user', 'is_approved']
