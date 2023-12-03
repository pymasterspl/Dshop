import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.fixture
def password_change_url():
    return reverse('api-password-change')


@pytest.fixture
def password_change_data():
    return {
        'current_password': 'testpassword',
        'new_password': 'new_testpassword',
        'new_password_again': 'new_testpassword',
    }


@pytest.mark.django_db
def test_password_change_success(
        api_client,
        password_change_url,
        user_instance_token,
        password_change_data,
        login_data,
        login_url
):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data)
    assert response.status_code == status.HTTP_200_OK

    # set new login data after password change and perform login
    login_data['password'] = password_change_data['new_password']
    response = api_client.post(login_url, login_data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_password_change_failure(api_client, password_change_url, user_instance_token, password_change_data):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data)
    assert response.status_code == status.HTTP_200_OK

    # after successful password change, current_password in password_change_data is no longer valid
    response = api_client.post(password_change_url, password_change_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_change_empty_token(api_client, password_change_url):
    api_client.credentials(HTTP_AUTHORIZATION='Token ')
    response = api_client.post(password_change_url, data={})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1


@pytest.mark.django_db
def test_password_change_empty_data(api_client, password_change_url, user_instance_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, data={})
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
    response = api_client.post(password_change_url, password_change_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1
    assert "current_password" in field_errors


@pytest.mark.django_db
def test_password_change_no_current_password(api_client, password_change_url, user_instance_token, password_change_data):
    del password_change_data['current_password']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1
    assert "current_password" in field_errors


@pytest.mark.django_db
def test_password_change_no_new_password(api_client, password_change_url, user_instance_token, password_change_data):
    del password_change_data['new_password']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1
    assert "new_password" in field_errors


@pytest.mark.django_db
def test_password_change_no_new_password_and_password_again(api_client, password_change_url, user_instance_token, password_change_data):
    del password_change_data['new_password']
    del password_change_data['new_password_again']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.post(password_change_url, password_change_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 2
    assert "new_password" in field_errors
    assert "new_password_again" in field_errors