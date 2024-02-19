import pytest
import json
from pytest import mark
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.products_catalogue.models import Order


@pytest.fixture
def fixture_order(tv_product, fixture_cart, fixture_delivery_method):

    client = APIClient()
    user = User.objects.create_user(username='testuser2', password='testpassword')
    client.force_authenticate(user)
    delivery = fixture_delivery_method
    cart = fixture_cart
    order = Order()

    cart_items = []
    cart_item = {}
    for item in cart:
        cart_item = { 
            'Product ID': str(item.product.pk),
            'Product': str(item.product),
            'Product-description': str(item.product.short_description),
            'Price': float(item.price),
            'Quantity': int(item.quantity),
            'Subtotal': float(item.subtotal),
            }
    cart_items.append(cart_item)
    
    order.cart_details = json.dumps(cart_items)
    order.delivery = fixture_delivery_method
    order.delivery_name = delivery.name
    order.delivery_price = delivery.price
    order.cart_total = cart.total
    order.total_sum = float(cart.total) + float(delivery.price)
    order.user = user
    order.save()
    return order


@mark.dj_shop_cart
@pytest.mark.django_db
def test_create_order( tv_product, fixture_cart, fixture_delivery_method):
    
    client = APIClient()
    user = User.objects.create_user(username='testuser2', password='testpassword')
    client.force_authenticate(user)
    delivery = fixture_delivery_method
    cart = fixture_cart
    order = Order()

    cart_items = []
    cart_item = {}
    for item in cart:
        cart_item = { 
            'Product ID': str(item.product.pk),
            'Product': str(item.product),
            'Product-description': str(item.product.short_description),
            'Price': float(item.price),
            'Quantity': int(item.quantity),
            'Subtotal': float(item.subtotal),
            }
    cart_items.append(cart_item)
    
    order.cart_details = json.dumps(cart_items)
    order.delivery = fixture_delivery_method
    order.delivery_name = delivery.name
    order.delivery_price = delivery.price
    order.cart_total = cart.total
    order.total_sum = float(cart.total) + float(delivery.price)
    order.user = user
    order.save()
    assert isinstance(order, Order)
    
