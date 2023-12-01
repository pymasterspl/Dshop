from django.contrib.auth import authenticate, get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import CustomUser

User = get_user_model()


class EmptySerializer(serializers.Serializer):
    pass


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
            password_validation.validate_password(attrs['password'])
        return attrs

    def save(self, **kwargs):
        validated_data = self.validated_data
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


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
        attrs['user'] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_again = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(_('Current password does not match'))
        return value

    def validate(self, attrs):
        if attrs['new_password'] and attrs['new_password_again']:
            if attrs['new_password'] != attrs['new_password_again']:
                raise ValidationError(_('Passwords does not match!'))
            password_validation.validate_password(attrs['new_password'])
        return attrs


class UserDataReadSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    user_email = serializers.EmailField(required=False, write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'user',
            'email',
            'user_email',
            'first_name',
            'last_name',
            'address',
            'postal_code',
            'city',
            'country',
            'date_of_birth',
            'phone_number'
        )


class UserDataChangeSerializer(UserDataReadSerializer):

    def update(self, instance, validated_data):
        # Update User fields
        user = instance.user
        if 'user_email' in validated_data:
            user.email = validated_data.pop('user_email')
            user.save()

        # Update CustomUser fields
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
