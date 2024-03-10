import datetime
from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient
from apps.products_catalogue.models import Category, Product


@pytest.fixture
def products():
    category = Category.objects.create(name='Test Category', is_active=True)
    for idx in range(1, 11):
        created_at = datetime.datetime.now() - datetime.timedelta(seconds=idx)
        Product.objects.create(
            name=f"main product ${idx}",
            category=category,
            price=idx,
            short_description="short desc inactive",
            full_description="full_description inactive",
            is_active=True,
            availability=3,
            created_at = created_at
        )
