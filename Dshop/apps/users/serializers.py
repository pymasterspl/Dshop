from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    """
    Serializer related to registration of a new user
    """
    username = serializers.CharField(min_length=2, max_length=255)
    email = serializers.EmailField(max_length=255)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('This username already exists'))
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('This email already exists'))
        return email

    def validate(self, attrs):
        # check if passwords are matching
        if attrs['password1'] and attrs['password2']:
            if attrs['password1'] != attrs['password2']:
                raise ValidationError(_('Passwords does not match!'))
        return attrs

    def get_cleaned_data(self):
        """
        Returns cleaned data.
        """
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password1', ''),
        }