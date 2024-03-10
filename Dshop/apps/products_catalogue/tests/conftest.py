import time

from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient
from apps.products_catalogue.models import Category, Product


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
            is_active=True,
            availability=3
        )
        time.sleep(0.2)
