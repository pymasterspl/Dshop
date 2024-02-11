from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient
from rest_framework import status


def assert_products_data(data, products, quantities):
    assert len(products) == len(quantities)
    items = data['items']
    count = 0
    total = Decimal("0")
    for product, quantity in zip(products, quantities):
        for item in items:
            if item['product_pk'] == product.pk:
                data_item = item
                break
        assert data_item['quantity'] == quantity
        assert Decimal(data_item['price']) == product.price
        assert data_item['product_name'] == product.name
        assert Decimal(data_item['subtotal'])
        total += Decimal(product.price) * quantity
        count += quantity
    assert Decimal(data['total']) == total
    assert data['count'] == count


def assert_data_empty(data):
    assert data['total'] == '0.00'
    assert data['count'] == 0
    assert data['items'] == []


@pytest.mark.django_db
def test_get_cart_empty(api_client_authed):
    response = api_client_authed.get(reverse("api_cart"))
    assert response.status_code == status.HTTP_200_OK
    assert_data_empty(response.data)


@pytest.mark.django_db
def test_add(api_client_authed, tv_product):
    data = {
        'items': [ {'product_pk': tv_product.pk, 'quantity': 10} ] 
    }
    response = api_client_authed.post(reverse("api_cart"), data)
    assert_products_data(response.data, [tv_product], [10])
    assert response.status_code == status.HTTP_201_CREATED
    response = api_client_authed.get(reverse("api_cart"))
    assert response.status_code == status.HTTP_200_OK
    assert_products_data(response.data, [tv_product], [10])


@pytest.mark.django_db
def test_add_relogin_get(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    data = {
        'items': [ {'product_pk': tv_product.pk, 'quantity': 10} ] 
    }
    response = client.post(reverse("api_cart"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert_products_data(response.data, [tv_product], [10])
    client.force_authenticate(user=None)
    client.force_authenticate(user)
    
    response = client.get(reverse("api_cart"))
    assert response.status_code == status.HTTP_200_OK
    assert_products_data(response.data, [tv_product], [10])
    

@pytest.mark.django_db
def test_add_ten_and_get(api_client_authed, ten_tv_products):
    quantities = [1, 1, 6, 8, 3, 4, 2, 26, 1, 10]

    data = {   
    'items': [
            {'product_pk': product.pk, 'quantity': quantity}
            for product, quantity in zip(ten_tv_products, quantities)
        ]
    }
    response = api_client_authed.post(reverse("api_cart"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert_products_data(response.data, ten_tv_products, quantities)
    response = api_client_authed.get(reverse("api_cart"))
    assert response.status_code == status.HTTP_200_OK
    assert_products_data(response.data, ten_tv_products, quantities)


@pytest.mark.django_db
def test_add_ten_replace_with_one(api_client_authed, ten_tv_products, tv_product):
    quantities = [11, 1, 3, 8, 4, 5, 6, 7, 1, 10]
    data = {   
        'items': [
                {'product_pk': product.pk, 'quantity': quantity}
                for product, quantity in zip(ten_tv_products, quantities)
            ]
        }
    response = api_client_authed.post(reverse("api_cart"), data)
    assert response.status_code == status.HTTP_201_CREATED

    data = {
        'items' : [
            {'product_pk': tv_product.pk, 'quantity': 666}
        ]
    }
    response = api_client_authed.post(reverse("api_cart"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert_products_data(response.data, [tv_product], [666])
    response = api_client_authed.get(reverse("api_cart"))
    assert response.status_code == status.HTTP_200_OK
    assert_products_data(response.data, [tv_product], [666])


@pytest.mark.django_db
def test_delete_ten(api_client_authed, ten_tv_products):
    quantities = [1, 1, 6, 8, 3, 4, 2, 26, 1, 10]
    data = {   
    'items': [
            {'product_pk': product.pk, 'quantity': quantity}
            for product, quantity in zip(ten_tv_products, quantities)
        ]
    }
    response = api_client_authed.post(reverse("api_cart"), data)
    assert response.status_code == status.HTTP_201_CREATED
    response = api_client_authed.post(reverse("api_cart"), {})
    assert response.status_code == status.HTTP_201_CREATED
    assert_data_empty(response.data)
    response = api_client_authed.get(reverse("api_cart"))
    assert_data_empty(response.data)


@pytest.mark.django_db
def test_get_non_unique_pks(api_client_authed, tv_product):
    data = {
        'items':[
            {'product_pk': tv_product.pk, 'quantity': 2},
            {'product_pk': tv_product.pk, 'quantity': 3}
        ]
    }
    response = api_client_authed.post(reverse("api_cart"), data)
    assert str(response.data['items'][0]) == "product_pk must be unique within items."
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_non_existing_pks(api_client_authed, tv_product):
    NON_EXISTING_ID = 999999
    data = {
        'items':[
            {'product_pk': tv_product.pk, 'quantity': 2},
            {'product_pk': NON_EXISTING_ID, 'quantity': 3}
        ]
    }
    response = api_client_authed.post(reverse("api_cart"), data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = api_client_authed.get(reverse("api_cart"))
    assert_data_empty(response.data)


@pytest.mark.django_db
def test_get_zero_quantities(api_client_authed, tv_product):
    data = {
        'items':[
            {'product_pk': tv_product.pk, 'quantity': 0}
        ]
    }
    response = api_client_authed.post(reverse("api_cart"), data)
    error_str = str(response.data['items'][0]['quantity'][0])
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert error_str == 'Ensure this value is greater than or equal to 1.'
