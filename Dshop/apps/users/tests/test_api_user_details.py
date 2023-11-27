import json

import pytest
from django.urls import reverse
from rest_framework import status

from ..models import CustomUser


@pytest.fixture
def user_details_change_url():
    return reverse('api-user-details')


@pytest.fixture()
def custom_user_instance(user_instance):
    return CustomUser.objects.create(user=user_instance)


@pytest.mark.django_db
def test_user_details_get_success(api_client, user_details_change_url, custom_user_instance, user_instance_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    response = api_client.get(user_details_change_url)
    assert response.status_code == status.HTTP_200_OK

    response_content = response.data
    assert response_content['user'] == custom_user_instance.user.id
    assert response_content['country'] == custom_user_instance.country
    assert response_content['email'] == custom_user_instance.user.email
    assert response_content['first_name'] == custom_user_instance.first_name
    assert response_content['last_name'] == custom_user_instance.last_name
    assert response_content['address'] == custom_user_instance.address
    assert response_content['postal_code'] == custom_user_instance.postal_code
    assert response_content['city'] == custom_user_instance.city
    assert response_content['date_of_birth'] == custom_user_instance.date_of_birth
    assert response_content['phone_number'] == custom_user_instance.phone_number


@pytest.mark.django_db
def test_user_details_empty_token(api_client, user_details_change_url, user_instance_token, custom_user_instance):
    api_client.credentials(HTTP_AUTHORIZATION='Token ')
    get_response = api_client.get(user_details_change_url)
    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED

    get_response = api_client.patch(user_details_change_url, data={})
    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_details_patch_success(api_client, user_details_change_url, user_instance_token, custom_user_instance):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    data = {
        'first_name': "test_name",
        'city': "test_city"
    }
    response = api_client.patch(user_details_change_url, data)
    assert response.status_code == status.HTTP_200_OK

    response_content = json.loads(response.content)
    custom_user = CustomUser.objects.get(user=user_instance_token.user)
    assert response_content['first_name'] == "test_name"
    assert response_content['city'] == "test_city"

    assert custom_user.first_name == "test_name"
    assert custom_user.city == "test_city"