from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': 'custom required message'}
        self.fields['password1'].error_messages = {
            'required': 'custom required password'}
        self.fields['email'].error_messages = {
            'required': 'custom required email'}
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     "placeholder": "e.g. Luke"})
        self.fields['password1'].widget.attrs.update({'class': 'form-control',
                                                      "placeholder": "Password"})
        self.fields['password2'].widget.attrs.update({'class': 'form-control',
                                                      "placeholder": "Password Confirmation"})
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  "placeholder": "e.g. Dshop@email.com"})


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ['user', 'date_joined']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
