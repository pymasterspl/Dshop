import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


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


@pytest.mark.django_db
def test_login_success(api_client, login_url, login_data, user_instance, user_instance_token):
    response = api_client.post(login_url, login_data, format='json')
    content = json.loads(response.content.decode('utf-8'))
    assert response.status_code == status.HTTP_200_OK
    assert content['username'] == user_instance.username
    assert content['email'] == user_instance.email
    assert content['token'] == user_instance_token.key


@pytest.mark.django_db
def test_login_empty_data(api_client, login_url):
    response = api_client.post(login_url, {}, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 2
    assert "username" in field_errors
    assert "password" in field_errors


@pytest.mark.django_db
def test_login_with_only_username(api_client, login_url, user_instance):
    response = api_client.post(login_url, {'username': 'testuser'}, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 1
    assert "password" in field_errors


@pytest.mark.django_db
def test_login_with_only_password(api_client, login_url, user_instance):
    response = api_client.post(login_url, {'password': 'testpassword'}, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 1
    assert "username" in field_errors


@pytest.mark.django_db
def test_login_with_username_and_empty_password(api_client, login_url, login_data, user_instance):
    login_data['password'] = ''
    response = api_client.post(login_url, login_data, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 1
    assert "password" in field_errors


@pytest.mark.django_db
def test_login_wrong_password(api_client, login_url, login_data, user_instance):
    login_data['password'] = 'different_password'
    response = api_client.post(login_url, login_data, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 1
