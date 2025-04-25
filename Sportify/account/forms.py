from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Athlete, Club
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.id  # Get the current user's ID

        if User.objects.exclude(id=user_id).filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

class ClubUserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.id

        # Check if the username already exists for another user
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            raise forms.ValidationError("A user with that username already exists.")
        
        return username

class AthleteSignupForm(forms.ModelForm):
    class Meta:
        model = Athlete
        exclude = ['user']

class ClubSignupForm(forms.ModelForm):
    class Meta:
        model = Club
        exclude = ['user', 'is_approved']
