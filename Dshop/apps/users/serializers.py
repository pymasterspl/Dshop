from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer related to registration of a new user
    """
    password = serializers.CharField(write_only=True)
    password_again = serializers.CharField(write_only=True)

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