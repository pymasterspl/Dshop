import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def login_url():
    return reverse('api-login')


@pytest.fixture
def login_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
    }


@pytest.fixture
def user_instance(login_data):
    return User.objects.create_user(**login_data)


@pytest.fixture
def user_instance_token(user_instance):
    return Token.objects.get_or_create(user=user_instance)[0]