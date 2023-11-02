import pytest
from django.urls import reverse
from pytest import mark

from dj_shop_cart.cart import get_cart_class


@mark.dj_shop_cart
@pytest.mark.django_db
def test_products_cart(tv_product, fake_cart_detail_view_request):
    Cart = get_cart_class()
    quantity = 2
    cart = Cart.new(fake_cart_detail_view_request)
    cart.add(tv_product, quantity=quantity)

    assert len(cart) == 1
    assert cart.count == 2


@mark.dj_shop_cart
@pytest.mark.django_db
def test_two_the_same_products_cart(tv_product, fake_cart_detail_view_request):
    Cart = get_cart_class()
    quantity = 4
    cart = Cart.new(fake_cart_detail_view_request)
    cart.add(tv_product, quantity=quantity)

    assert len(cart) == 1
    assert cart.count == 4


@mark.dj_shop_cart
@pytest.mark.django_db
def test_two_different_products_cart(
        tv_product, edifier_product,
        fake_cart_detail_view_request
):
    Cart = get_cart_class()
    quantity_1 = 1
    cart = Cart.new(fake_cart_detail_view_request)
    cart.add(tv_product, quantity=quantity_1)

    quantity_2 = 2
    cart = Cart.new(fake_cart_detail_view_request)
    cart.add(edifier_product, quantity=quantity_2)

    assert len(cart) == 2
    assert cart.count == 3


@mark.dj_shop_cart
@pytest.mark.django_db
def test_response_add_to_cart_view_request(client, tv_product):
    url = reverse(
        'add_to_cart_view',
        kwargs={
            'slug': 'first-one',
            'id': tv_product.id
        }
    )
    fake_response = client.get(url)

    assert fake_response.status_code == 302
    assert fake_response.url == reverse('cart_detail_view')


@mark.dj_shop_cart
@pytest.mark.django_db
def test_add_non_exist_product_to_cart(client):
    url = reverse(
        'add_to_cart_view',
        kwargs={
            'slug': 'first-one',
            'id': 999
        }
    )
    fake_response = client.get(url)

    assert fake_response.status_code == 404


@mark.dj_shop_cart
@pytest.mark.django_db
def test_add_product_to_cart(tv_product, fake_add_to_cart_view_request):
    Cart = get_cart_class()
    cart = Cart.new(fake_add_to_cart_view_request)

    assert len(cart) == 1
    assert cart.count == 1
    assert cart.find_one(product=tv_product).product == tv_product
    assert tv_product in cart.products


@mark.dj_shop_cart
@pytest.mark.django_db
def test_cart_increase_quantity(tv_product, fake_add_to_cart_view_request):
    Cart = get_cart_class()
    cart = Cart.new(fake_add_to_cart_view_request)
    item = cart.add(product=tv_product, quantity=10)
    item = cart.increase(item.id, quantity=10)  # I dont know how to use it yet
    assert item.quantity == 21
