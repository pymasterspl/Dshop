import pytest
from django.contrib import messages
from django.urls import reverse
from pytest import mark

from dj_shop_cart.cart import get_cart_class


@pytest.fixture
def fixture_cart(tv_product, edifier_product, fake_cart_detail_view_request):
    Cart = get_cart_class() 
    cart = Cart.new(fake_cart_detail_view_request)
    cart.add(tv_product, quantity=2)
    cart.add(edifier_product, quantity=3)
    return cart


@pytest.mark.django_db
def test_fixture_cart(fixture_cart):
    Cart = get_cart_class() 
    assert isinstance(fixture_cart, Cart)


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
def test_two_the_same_products_cart(tv_product, fake_add_to_cart_view_request):
    Cart = get_cart_class()
    cart = Cart.new(fake_add_to_cart_view_request)

    assert len(cart) == 1
    assert cart.count == 1


@mark.dj_shop_cart
@pytest.mark.django_db
def test_add_two_different_products_cart(
        tv_product, edifier_product,
        fake_add_to_cart_view_request
):
    Cart = get_cart_class()
    quantity_1 = 2
    cart = Cart.new(fake_add_to_cart_view_request)
    cart.add(tv_product, quantity=quantity_1)

    quantity_2 = 3
    cart.add(edifier_product, quantity=quantity_2)

    assert len(cart) == 2
    assert cart.count == 6


@mark.dj_shop_cart
@pytest.mark.django_db
def test_response_add_to_cart_view_request(client, tv_product):
    url = reverse(
        'add_to_cart',
        kwargs={
            'slug': 'first-one',
            'id': tv_product.id,
            'quantity': 1
        }
    )
    fake_response = client.post(url)

    assert fake_response.status_code == 302
    assert fake_response.url == reverse('cart_detail')


@mark.dj_shop_cart
@pytest.mark.django_db
def test_add_non_exist_product_to_cart(client):
    url = reverse(
        'add_to_cart',
        kwargs={
            'slug': 'first-one',
            'id': 999,
            'quantity': 1
        }
    )
    fake_response = client.post(url)

    assert fake_response.status_code == 404


@mark.dj_shop_cart
@pytest.mark.django_db
def test_response_add_to_cart_zero_view_request(client, tv_product):
    url = reverse(
        'add_to_cart',
        kwargs={
            'slug': 'first-one',
            'id': tv_product.id,
            'quantity': 0
        }
    )
    fake_response = client.post(url)
    msg = [m.message for m in messages.get_messages(fake_response.wsgi_request)]

    assert fake_response.status_code == 302
    assert "Ilość musi być większa niż 0." in msg
    assert fake_response.url == reverse('cart_detail')


@mark.dj_shop_cart
@pytest.mark.django_db
def test_response_add_to_cart_minus_view_request(client, tv_product):
    url = reverse(
        'add_to_cart',
        kwargs={
            'slug': 'first-one',
            'id': tv_product.id,
            'quantity': -1
        }
    )
    fake_response = client.post(url)
    msg = [m.message for m in messages.get_messages(fake_response.wsgi_request)]

    assert fake_response.status_code == 302
    assert "Ilość musi być większa niż 0." in msg
    assert fake_response.url == reverse('cart_detail')


@mark.dj_shop_cart
@pytest.mark.django_db
def test_response_add_to_cart_view_request_no_message(client, fake_add_to_cart_view_request):
    Cart = get_cart_class()
    cart = Cart.new(fake_add_to_cart_view_request)

    msg = [m.message for m in messages.get_messages(fake_add_to_cart_view_request)]

    assert len(cart) == 1
    assert cart.count == 1
    assert "Ilość musi być większa niż 0." not in msg


@mark.dj_shop_cart
@pytest.mark.django_db
def test_response_add_to_cart_view_request_ok_quantity(
        client,
        tv_product,
        fake_cart_detail_view_request,
        fake_add_to_cart_view_request
):
    Cart = get_cart_class()
    cart = Cart.new(fake_cart_detail_view_request)

    assert len(cart) == 0
    assert cart.count == 0

    cart = Cart.new(fake_add_to_cart_view_request)

    assert len(cart) == 1
    assert cart.count == 1
