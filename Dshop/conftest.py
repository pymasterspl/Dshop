import pytest
from dj_shop_cart.cart import get_cart_class
from django.urls import reverse
from pytest import fixture

from apps.products_catalogue.models import Category, Product


@fixture()
@pytest.mark.django_db
def product():
    category = Category.objects.create(
        name='Test Category',
        is_active=True
    )
    product = Product.objects.create(
        name='TV AMOLED',
        price=3999.00,
        full_description='Description 1',
        category=category
    )
    return product


@fixture
def fake_request(client):
    url = reverse(
        "cart_detail_view"
    )
    fake_response = client.get(url)
    fake_request = fake_response.wsgi_request

    return fake_request
