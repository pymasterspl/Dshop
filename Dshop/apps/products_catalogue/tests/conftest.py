from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient
from apps.products_catalogue.models import Category, Product


@pytest.fixture
def api_client():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    return client


@pytest.fixture
def products():
    category = Category.objects.create(name='Test Category', is_active=True)
    for price in range(1, 11):
        Product.objects.create(
            name=f"main product ${price}",
            category=category,
            price=price,
            short_description="short desc inactive",
            full_description="full_description inactive",
            is_active=True
        )

