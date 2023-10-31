import pytest
from django.urls import reverse
from pytest import fixture

from apps.products_catalogue.models import Category, Product


@fixture()
@pytest.mark.django_db
def tv_product():
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


@fixture()
@pytest.mark.django_db
def edifier_product():
    category = Category.objects.create(
        name='Test Category',
        is_active=True
    )
    product = Product.objects.create(
        name='Edifier r1700dbs',
        price=499.00,
        full_description='Description 2',
        category=category
    )
    return product


@fixture
def fake_cart_detail_view_request(client):
    url = reverse(
        "cart_detail_view"
    )
    fake_response = client.get(url)
    fake_request = fake_response.wsgi_request

    return fake_request


@fixture
def fake_add_to_cart_view_request(client, tv_product):
    url = reverse(
        'add_to_cart_view',
        kwargs={
            'slug': 'first-one',
            'id': tv_product.id,
        }
    )
    fake_response = client.get(url)
    fake_add_request = fake_response.wsgi_request

    return fake_add_request
