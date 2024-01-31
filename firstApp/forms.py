from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import myUserDB

class SignUpForm(UserCreationForm):
    class Meta:
        model = myUserDB
        fields = ['username', 'bio']

class LoginForm(AuthenticationForm):
    class Meta:
        model = myUserDB
        fields = ['username', 'password']