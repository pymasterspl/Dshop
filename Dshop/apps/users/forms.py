from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class LoginUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ['user', 'date_joined']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
