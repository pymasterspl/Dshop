from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer related to registration of a new user
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] and attrs['password2']:
            if attrs['password1'] != attrs['password2']:
                raise ValidationError(_('Passwords does not match!'))
        return attrs