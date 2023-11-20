import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from pytest import mark


from dj_shop_cart.cart import get_cart_class, Cart


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
def test_delete_element_item_cart(
        fake_delete_to_cart_view_request,
        item_cart,
):
    """
    It doesn't work. I don't know why
    """
    item, cart = item_cart
    assert len(cart) == 1
    assert cart.count == 4

    cart = Cart.new(fake_delete_to_cart_view_request)

    assert len(cart) == 1
    assert item.quantity == 2
