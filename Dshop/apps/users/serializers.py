from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer related to registration of a new user
    """
    password = serializers.CharField(style={'input_type': 'password'})
    password_again = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_again')

    def validate(self, attrs):
        if attrs['password'] and attrs['password_again']:
            if attrs['password'] != attrs['password_again']:
                raise ValidationError(_('Passwords does not match!'))
            else:
                # delete arg password_again because User model does not accept it upon serializer.save()
                del attrs['password_again']
        return attrs


class LoginSerializer(serializers.Serializer):
    """
    Login Serializer for User model
    """
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.pop('username')
        password = attrs.pop('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError(_('Unable to log in with provided credentials'))
        if not user.is_active:
            raise ValidationError(_('User account is disabled.'))

        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """
    class Meta:
        model = Token
        fields = ('key',)