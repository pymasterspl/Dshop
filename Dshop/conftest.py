from importlib import import_module

import pytest
from dj_shop_cart.cart import get_cart_class
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.urls import reverse
from django.conf import settings
from django.test import Client

from apps.products_catalogue.models import Category, Product
from apps.users.models import CustomUser

# User = CustomUser
Cart = get_cart_class()
User = get_user_model()


@pytest.fixture()
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


@pytest.fixture()
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


@pytest.fixture()
def fake_cart_detail_view_request(client, session):
    url = reverse(
        "cart_detail_view"
    )
    print(session)
    fake_response = client.get(url)
    fake_response.user = AnonymousUser()
    fake_response.session = session
    print(fake_response.session)
    fake_request = fake_response

    return fake_request


@pytest.fixture()
def session() -> SessionBase:
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore()


@pytest.fixture()
def user(django_user_model: type[User]):
    return django_user_model.objects.create(username="someone", password="password")


@pytest.fixture()
def item_cart(fake_cart_detail_view_request, tv_product):
    Cart = get_cart_class()
    quantity_1 = 4
    cart = Cart.new(fake_cart_detail_view_request)
    item = cart.add(tv_product, quantity=quantity_1)

    return item, cart


@pytest.fixture()
def fake_add_to_cart_view_request(client, tv_product, session):
    url = reverse(
        'add_to_cart_view',
        kwargs={
            'slug': tv_product.slug,
            'id': tv_product.id,
        }
    )

    fake_response = client.get(url)
    fake_add_request = fake_response.wsgi_request

    return fake_add_request


@pytest.fixture()
def fake_delete_to_cart_view_request(client,tv_product, item_cart, session):
    item, cart = item_cart

    url = reverse(
        'delete_one_cart_item_view',
        kwargs={
            'slug': tv_product.slug,
            'item_id': item.id,
        }
    )
    client = Client()
    client._session = session

    fake_response = client.get(url)
    fake_response.user = AnonymousUser()
    fake_response.session = session

    return fake_response
