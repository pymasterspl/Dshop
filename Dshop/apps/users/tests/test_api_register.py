import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from ..models import CustomUser

User = get_user_model()


@pytest.fixture
def registration_url():
    return reverse('api-register')


@pytest.fixture
def registration_data():
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
        'password_again': 'testpassword',
    }


@pytest.mark.django_db
def test_registration_success(api_client, registration_url, registration_data):
    response = api_client.post(registration_url, registration_data, format='json')
    content = json.loads(response.content.decode('utf-8'))
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(username='testuser')

    assert content['username'] == user.username
    assert content['email'] == user.email
    assert user.username == registration_data['username']
    assert user.email == registration_data['email']

    assert User.objects.count() == 1
    assert CustomUser.objects.count() == 1


@pytest.mark.django_db
def test_empty_data(api_client, registration_url):
    response = api_client.post(registration_url, data={}, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 3
    assert "username" in field_errors
    assert "password" in field_errors
    assert "password_again" in field_errors


@pytest.mark.django_db
def test_missing_username(api_client, registration_url, registration_data):
    registration_data['username'] = ''
    response = api_client.post(registration_url, data=registration_data, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 1
    assert "username" in field_errors


@pytest.mark.django_db
def test_username_already_exists_failure(api_client, registration_url, registration_data):
    api_client.post(registration_url, registration_data, format='json')
    response = api_client.post(registration_url, registration_data, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 1
    assert "username" in field_errors


@pytest.mark.django_db
def test_not_matching_passwords_failure(api_client, registration_url, registration_data):
    registration_data['password_again'] = 'changed_password'
    response = api_client.post(registration_url, registration_data, format='json')
    field_errors = json.loads(response.content).keys()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert CustomUser.objects.count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(field_errors) == 1


@pytest.mark.django_db
def test_missing_second_password(api_client, registration_url, registration_data):
    registration_data['password_again'] = ''
    response = api_client.post(registration_url, data=registration_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    field_errors = json.loads(response.content).keys()
    assert len(field_errors) == 1
    assert "password_again" in field_errors


@pytest.mark.django_db
def test_missing_email(api_client, registration_url, registration_data):
    registration_data['email'] = ''
    response = api_client.post(registration_url, data=registration_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED