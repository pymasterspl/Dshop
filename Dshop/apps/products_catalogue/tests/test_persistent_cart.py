import pytest
from pytest import mark

from dj_shop_cart.cart import get_cart_class


@mark.dj_shop_cart
@pytest.mark.django_db
def test_products_cart(product, fake_request):
    Cart = get_cart_class()

    quantity = 2
    cart = Cart.new(fake_request)
    cart.add(product, quantity=quantity)

    assert len(cart) == 1
    assert cart.count == 2
