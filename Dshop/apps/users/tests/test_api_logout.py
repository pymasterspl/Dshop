import json

import pytest
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


@pytest.fixture
def logout_url():
    return reverse('api-logout')


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


@pytest.mark.django_db
def test_logout_success(api_client, logout_url, user_instance, user_instance_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    logout_response = api_client.post(logout_url)
    assert logout_response.status_code == status.HTTP_200_OK

    authenticated_user = authenticate(user_instance=user_instance, token_key=user_instance_token.key)
    assert authenticated_user is None

    with pytest.raises(user_instance_token.DoesNotExist):
        Token.objects.get(user=user_instance)


@pytest.mark.django_db
def test_logout_success_without_credentials(api_client, logout_url):
    # If user is not logged in, response should be also 200 because user is already logged out
    logout_response = api_client.post(logout_url)
    assert logout_response.status_code == status.HTTP_200_OK