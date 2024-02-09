from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    return client