import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


@pytest.fixture
def password_change_url():
    return reverse('api-password-change')


@pytest.fixture
def login_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
    }


@pytest.fixture
def password_change_data():
    return {
        'current_password': 'testpassword',
        'new_password': 'new_testpassword',
        'new_password_again': 'new_testpassword',
    }


@pytest.fixture
def user_instance(login_data):
    return User.objects.create_user(**login_data)


@pytest.fixture
def user_instance_token(user_instance):
    return Token.objects.get_or_create(user=user_instance)[0]


@pytest.mark.django_db
def test_password_change_success(api_client, password_change_url, user_instance_token, password_change_data):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data, format='json')
    assert response.status_code == status.HTTP_200_OK

    response = api_client.post(password_change_url, password_change_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_change_empty_token(api_client, password_change_url):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token ')
    response = api_client.post(password_change_url, {}, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1


@pytest.mark.django_db
def test_password_change_empty_data(api_client, password_change_url, user_instance_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 3
    assert "current_password" in field_errors
    assert "new_password" in field_errors
    assert "new_password_again" in field_errors


@pytest.mark.django_db
def test_password_change_wrong_current_password(api_client, password_change_url, user_instance_token, password_change_data):
    password_change_data['current_password'] = 'wrong_current_password'
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1
    assert "current_password" in field_errors


@pytest.mark.django_db
def test_password_change_no_current_password(api_client, password_change_url, user_instance_token, password_change_data):
    del password_change_data['current_password']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1
    assert "current_password" in field_errors


@pytest.mark.django_db
def test_password_change_no_new_password(api_client, password_change_url, user_instance_token, password_change_data):
    del password_change_data['new_password']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1
    assert "new_password" in field_errors


@pytest.mark.django_db
def test_password_change_no_new_password_and_password_again(api_client, password_change_url, user_instance_token, password_change_data):
    del password_change_data['new_password']
    del password_change_data['new_password_again']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 2
    assert "new_password" in field_errors
    assert "new_password_again" in field_errors