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


@pytest.mark.django_db
def test_get_cart_detail():
    client = APIClient()
    url = reverse("api_cart")
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    response = client.get(url, {}, format="json")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.data
    assert response_data['total'] == "0.00"
    assert response_data['count'] == 0
    assert response_data['items'] == []


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