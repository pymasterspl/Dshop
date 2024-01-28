from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient
from rest_framework import status


def counts_to_price_quantity(products, quantities):
    assert len(products) == len(quantities)
    quant_map = enumerate(quantities)
    total_quantity = sum(quantities)
    total_price = sum(products[idx].price * quantity for idx, quantity in quant_map)
    return total_quantity, total_price

def assert_data_empty(data):
    assert data['total'] == '0.00'
    assert data['count'] == 0
    assert data['items'] == []


@pytest.mark.django_db
def test_get_cart_empty():
    client = APIClient()
    url = reverse("api_cart")
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    response = client.get(url, {}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert_data_empty(response.data)


@pytest.mark.django_db
def test_add(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    product = tv_product

    data = {
        'items': [ {'product_pk': product.pk, 'quantity': 10} ] 
    }
    response = client.post(reverse("api_cart"), data, format='json')
    data = response.data
    first_item = data["items"][0]
    assert response.status_code == status.HTTP_201_CREATED
    assert Decimal(data["total"]) ==  Decimal(first_item['subtotal']) == Decimal(tv_product.price * 10)  
    assert data["count"] == first_item["quantity"] == 10 
    assert first_item["product_name"] == product.name

@pytest.mark.django_db
def test_add_relogin_get(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    product = tv_product

    data = {
        'items': [ {'product_pk': product.pk, 'quantity': 10} ] 
    }
    client.force_authenticate(user=None)
    client.force_authenticate(user)
    response = client.post(reverse("api_cart"), data, format='json')
    data = response.data
    first_item = data["items"][0]
    assert response.status_code == status.HTTP_201_CREATED
    assert Decimal(data["total"]) ==  Decimal(first_item['subtotal']) == Decimal(tv_product.price * 10)  
    assert data["count"] == first_item["quantity"] == 10 
    assert first_item["product_name"] == product.name


@pytest.mark.django_db
def test_add_ten_and_get(ten_tv_products):
    client = APIClient()
    tvs = ten_tv_products
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    quantities = [1, 1, 6, 8, 3, 4, 2, 26, 1, 10]
    total_quantity, total_price = counts_to_price_quantity(tvs, quantities)

    data = {   
    'items': [
            {'product_pk': product.pk, 'quantity': quantity}
            for product, quantity in zip(ten_tv_products, quantities)
        ]
    }
    response = client.post(reverse("api_cart"), data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Decimal(response.data['total']) == Decimal(total_price)
    assert response.data['count'] == total_quantity


@pytest.mark.django_db
def test_delete_ten(ten_tv_products):
    client = APIClient()
    tvs = ten_tv_products
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    quantities = [1, 1, 6, 8, 3, 4, 2, 26, 1, 10]
    total_quantity, total_price = counts_to_price_quantity(tvs, quantities)

    data = {   
    'items': [
            {'product_pk': product.pk, 'quantity': quantity}
            for product, quantity in zip(ten_tv_products, quantities)
        ]
    }
    response = client.post(reverse("api_cart"), data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post(reverse("api_cart"), {}, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert_data_empty(response.data)


@pytest.mark.django_db
def test_get_non_unique_pks(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)

    data = {
        'items':[
            {'product_pk': tv_product.pk, 'quantity': 2},
            {'product_pk': tv_product.pk, 'quantity': 3}
        ]
    }
    response = client.post(reverse("api_cart"), data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_get_non_unique_pks(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    NON_EXISTING_ID = 999999
        
    data = {
        'items':[
            {'product_pk': tv_product.pk, 'quantity': 2},
            {'product_pk': NON_EXISTING_ID, 'quantity': 3}
        ]
    }
    response = client.post(reverse("api_cart"), data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.get(reverse("api_cart"), {}, format="json")
    assert_data_empty(response.data)


@pytest.mark.django_db
def test_add_check_subtotals(ten_tv_products):
    three_products = ten_tv_products[:3]
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    data = {
        'items':[
            {'product_pk': three_products[0].pk, 'quantity': 1},
            {'product_pk': three_products[1].pk, 'quantity': 5},
            {'product_pk': three_products[2].pk, 'quantity': 10},
        ]
    }
    response = client.post(reverse("api_cart"), data, format="json")
    assert Decimal(response.data['items'][0]['subtotal']) == three_products[0].price
    assert Decimal(response.data['items'][1]['subtotal']) == 5 * three_products[1].price
    assert Decimal(response.data['items'][2]['subtotal']) == 10 * three_products[2].price

@pytest.mark.django_db
def test_get_zero_quantities(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
        
    data = {
        'items':[
            {'product_pk': tv_product.pk, 'quantity': 0}
        ]
    }
    response = client.post(reverse("api_cart"), data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST