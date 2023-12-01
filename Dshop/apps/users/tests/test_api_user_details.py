import datetime
import json

import pytest
from django.urls import reverse
from rest_framework import status

from ..models import CustomUser, Country


@pytest.fixture
def user_details_url():
    return reverse('api-user-details')


@pytest.fixture()
def custom_user_instance(user_instance):
    return CustomUser.objects.create(user=user_instance)


@pytest.fixture()
def country_instance():
    return Country.objects.create(name="Poland", code="PL")


@pytest.fixture()
def user_details_data():
    return {
        "user_email": "test@pymasters.pl",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "address": "test_address",
        "postal_code": "123-456",
        "city": "test_city",
        "country": 1,
        "date_of_birth": "2023-12-01",
        "phone_number": "123 123 123"
        }


@pytest.mark.django_db
def test_get_user_details_success(api_client, user_details_url, custom_user_instance, user_instance_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.get(user_details_url)
    assert response.status_code == status.HTTP_200_OK

    response_content = response.data
    assert response_content['user'] == custom_user_instance.user.id
    assert response_content['email'] == custom_user_instance.user.email
    assert response_content['first_name'] == custom_user_instance.first_name
    assert response_content['last_name'] == custom_user_instance.last_name
    assert response_content['address'] == custom_user_instance.address
    assert response_content['postal_code'] == custom_user_instance.postal_code
    assert response_content['city'] == custom_user_instance.city
    assert response_content['country'] == custom_user_instance.country
    assert response_content['date_of_birth'] == custom_user_instance.date_of_birth
    assert response_content['phone_number'] == custom_user_instance.phone_number


@pytest.mark.django_db
def test_get_user_details_empty_token_failure(
        api_client,
        user_details_url,
        user_instance_token,
        custom_user_instance
):
    api_client.credentials(HTTP_AUTHORIZATION='Token ')
    get_response = api_client.get(user_details_url)
    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED

    get_response = api_client.patch(user_details_url, data={})
    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_put_user_details_success(
        api_client,
        user_details_url,
        user_details_data,
        user_instance_token,
        custom_user_instance,
        country_instance
):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.put(user_details_url, user_details_data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 10
    assert response.data['user'] == user_instance_token.user.id
    assert response.data['email'] == user_details_data['user_email']
    assert response.data['first_name'] == user_details_data['first_name']
    assert response.data['last_name'] == user_details_data['last_name']
    assert response.data['address'] == user_details_data['address']
    assert response.data['postal_code'] == user_details_data['postal_code']
    assert response.data['city'] == user_details_data['city']
    assert response.data['country'] == user_details_data['country']
    assert response.data['date_of_birth'] == user_details_data['date_of_birth']
    assert response.data['phone_number'] == user_details_data['phone_number']

    custom_user = CustomUser.objects.get(user=user_instance_token.user)
    assert custom_user.user.email == user_details_data['user_email']
    assert custom_user.first_name == user_details_data['first_name']
    assert custom_user.last_name == user_details_data['last_name']
    assert custom_user.address == user_details_data['address']
    assert custom_user.postal_code == user_details_data['postal_code']
    assert custom_user.city == user_details_data['city']
    assert custom_user.country.id == user_details_data['country']
    assert custom_user.date_of_birth.strftime("%Y-%m-%d") == user_details_data['date_of_birth']
    assert custom_user.phone_number == user_details_data['phone_number']


@pytest.mark.django_db
def test_put_user_details_with_empty_data(
        api_client,
        user_details_url,
        user_details_data,
        user_instance_token,
        custom_user_instance,
        country_instance
):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.put(user_details_url, data={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.data) == 6
    assert 'first_name' in response.data
    assert 'last_name' in response.data
    assert 'address' in response.data
    assert 'postal_code' in response.data
    assert 'city' in response.data
    assert 'phone_number' in response.data


@pytest.mark.django_db
def test_put_user_details_with_2_empty_fields(
        api_client,
        user_details_url,
        user_details_data,
        user_instance_token,
        custom_user_instance,
        country_instance
):
    user_details_data['first_name'] = ''
    user_details_data['phone_number'] = ''

    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.put(user_details_url, data=user_details_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.data) == 2
    assert 'first_name' in response.data
    assert 'phone_number' in response.data


@pytest.mark.django_db
def test_patch_user_details_success(
        api_client,
        user_details_url,
        user_details_data,
        user_instance_token,
        custom_user_instance,
        country_instance
):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.patch(user_details_url, user_details_data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 10
    assert response.data['user'] == user_instance_token.user.id
    assert response.data['email'] == user_details_data['user_email']
    assert response.data['first_name'] == user_details_data['first_name']
    assert response.data['last_name'] == user_details_data['last_name']
    assert response.data['address'] == user_details_data['address']
    assert response.data['postal_code'] == user_details_data['postal_code']
    assert response.data['city'] == user_details_data['city']
    assert response.data['country'] == user_details_data['country']
    assert response.data['date_of_birth'] == user_details_data['date_of_birth']
    assert response.data['phone_number'] == user_details_data['phone_number']

    custom_user = CustomUser.objects.get(user=user_instance_token.user)
    assert custom_user.user.email == user_details_data['user_email']
    assert custom_user.first_name == user_details_data['first_name']
    assert custom_user.last_name == user_details_data['last_name']
    assert custom_user.address == user_details_data['address']
    assert custom_user.postal_code == user_details_data['postal_code']
    assert custom_user.city == user_details_data['city']
    assert custom_user.country.id == user_details_data['country']
    assert custom_user.date_of_birth.strftime("%Y-%m-%d") == user_details_data['date_of_birth']
    assert custom_user.phone_number == user_details_data['phone_number']


@pytest.mark.django_db
def test_patch_user_details_with_empty_data(
        api_client,
        user_details_url,
        user_details_data,
        user_instance_token,
        custom_user_instance,
        country_instance
):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.patch(user_details_url, data={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.data) == 6
    assert 'first_name' in response.data
    assert 'last_name' in response.data
    assert 'address' in response.data
    assert 'postal_code' in response.data
    assert 'city' in response.data
    assert 'phone_number' in response.data


@pytest.mark.django_db
def test_patch_user_details_with_2_empty_fields(
        api_client,
        user_details_url,
        user_details_data,
        user_instance_token,
        custom_user_instance,
        country_instance
):
    user_details_data['first_name'] = ''
    user_details_data['phone_number'] = ''

    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.patch(user_details_url, data=user_details_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.data) == 2
    assert 'first_name' in response.data
    assert 'phone_number' in response.data