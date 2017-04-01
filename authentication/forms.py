from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username', 'autofocus': 'autofocus'}))
    password = forms.CharField(label="Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))