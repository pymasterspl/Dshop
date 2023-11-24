import pytest
from dj_shop_cart.cart import get_cart_class
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.base import SessionBase
from django.urls import reverse
from pytest import fixture
from django.test import RequestFactory

from apps.products_catalogue.models import Category, Product
from apps.users.models import CustomUser

User = CustomUser
Cart = get_cart_class()


@fixture
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


@fixture
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
        "cart_detail"
    )
    fake_response = client.get(url)
    fake_request = fake_response.wsgi_request

    return fake_request


@fixture
def fake_add_to_cart_view_request(client, tv_product):
    url = reverse(
        'add_to_cart',
        kwargs={
            'slug': tv_product.slug,
            'id': tv_product.id,
            'quantity': 1
        }
    )
    fake_response = client.post(url)
    fake_add_request = fake_response.wsgi_request

    return fake_add_request
