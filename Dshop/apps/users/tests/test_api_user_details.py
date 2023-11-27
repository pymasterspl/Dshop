import json

import pytest

from django.urls import reverse
from rest_framework import status


@pytest.fixture
def user_details_change_url():
    return reverse('api-update')


@pytest.mark.django_db
def test_user_details_change_success(api_client, user_details_change_url, user_instance_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')

    data = {
        'first_name': "First name",
    }
    response = api_client.patch(user_details_change_url, data, format='json')
    assert response.status_code == status.HTTP_200_OK