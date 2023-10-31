import pytest
from django.urls import reverse
from pytest import mark

from dj_shop_cart.cart import get_cart_class
from apps.products_catalogue.models import Category, Product


@mark.dj_shop_cart
@pytest.mark.django_db
def test_products_cart(client):
    Cart = get_cart_class()

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
    quantity = 2
    url = reverse(
        "cart_detail_view",

    )
    fake_response = client.get(url)
    fake_request = fake_response.wsgi_request

    cart = Cart.new(fake_request)
    cart.add(product, quantity=quantity)

    assert len(cart) == 1
    assert cart.count == 2
