import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
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


@pytest.mark.django_db
def test_login_success(api_client, login_url, login_data, user_instance):
    response = api_client.post(login_url, login_data, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_login_empty_data(api_client, login_url, user_instance):
    response = api_client.post(login_url, {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_with_only_username(api_client, login_url, user_instance):
    response = api_client.post(login_url, {'username': 'testuser'}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_with_only_password(api_client, login_url, user_instance):
    response = api_client.post(login_url, {'password': 'testpassword'}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_with_username_and_empty_password(api_client, login_url, login_data, user_instance):
    login_data['password'] = ''
    response = api_client.post(login_url, login_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_wrong_password(api_client, login_url, login_data, user_instance):
    login_data['password'] = 'different_password'
    response = api_client.post(login_url, login_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST