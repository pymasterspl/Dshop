from django.forms import ValidationError
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
    url = reverse("api_cart_detail")
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    response = client.get(url, {}, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    assert "total" in response.data
    assert "count" in response.data
    assert "items" in response.data


@pytest.mark.django_db
def test_add(tv_product):
    client = APIClient()
    product = tv_product
    add_url = reverse("api_add_to_cart", args=[product.id, 10])
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    response = client.post(add_url, {}, content_type="application/json")
    data = response.data
    first_item = data.get("items")[0]
    assert response.status_code == status.HTTP_201_CREATED
    assert data.get("total") == tv_product.price * 10 == first_item.get("subtotal")
    assert data.get("count") == 10 == first_item.get("quantity")
    assert first_item.get("product_name") == product.name


@pytest.mark.django_db
def test_add_relogin_get(tv_product):
    client = APIClient()
    product = tv_product
    add_url = reverse("api_add_to_cart", args=[product.id, 10])
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    client.post(add_url, {}, content_type="application/json")
    client.force_authenticate(user=None)
    client.force_authenticate(user)
    response = client.get(reverse("api_cart_detail"), data={}, content_type="application/jspm")
    data = response.data
    first_item = data.get("items")[0]
    assert response.status_code == status.HTTP_200_OK
    assert data.get("total") == tv_product.price * 10 == first_item.get("subtotal")
    assert data.get("count") == 10 == first_item.get("quantity")
    assert first_item.get("product_name") == product.name


@pytest.mark.django_db
def test_add_ten_and_get(ten_tv_products):
    client = APIClient()
    tvs = ten_tv_products
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    quantities = [1, 1, 6, 8, 3, 4, 2, 26, 1, 10]
    total_quantity, total_price = counts_to_price_quantity(tvs, quantities)
    for tv, quantity in zip(tvs, quantities):
        url = reverse("api_add_to_cart", args=[tv.id, quantity])
        client.post(url, {}, content_type="application/json")
    response = client.get(reverse("api_cart_detail"), {}, content_type="application/json")
    assert response.data['total'] == total_price
    assert response.data['count'] == total_quantity              


@pytest.mark.django_db
def test_delete_cart_delete_one(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    product = tv_product
    post_url = reverse("api_add_to_cart", kwargs={"id": product.id, "quantity": 10})
    response = client.post(post_url, {}, content_type="application/json")
    item_id = response.data['items'][0]['item_id']
    delete_url = reverse("api_delete_cart_items", kwargs={"item_id": item_id, "quantity": 6})
    reponse = client.delete(delete_url, {}, content_type="application/json")
    assert reponse.status_code == status.HTTP_204_NO_CONTENT
    response = client.get(reverse("api_cart_detail"), {}, content_type="application/json")
    assert response.data["count"] == 4


@pytest.mark.django_db
def test_delete_cart_all(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    product = tv_product
    post_url = reverse("api_add_to_cart", kwargs={"id": product.id, "quantity": 10})
    response = client.post(post_url, {}, content_type="application/json")
    item_id = response.data['items'][0]['item_id']
    delete_url = reverse("api_delete_all_cart_items", kwargs={"item_id": item_id})
    reponse = client.delete(delete_url, {}, content_type="application/json")
    assert reponse.status_code == status.HTTP_204_NO_CONTENT
    reponse = client.get(reverse("api_cart_detail"), {}, content_type="application/json")
    assert reponse.data["count"] == 0


@pytest.mark.django_db
def test_delete_cart_one_non_existing():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    delete_url = reverse("api_delete_cart_items", kwargs={"item_id": "XZYXZYZ", "quantity": 6})
    response = client.delete(delete_url, {}, content_type="application/json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_cart_all_non_existing():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    delete_url = reverse("api_delete_all_cart_items", kwargs={"item_id": "XZYXZYZ"})
    response = client.delete(delete_url, {}, content_type="application/json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_add_non_existing_product():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    post_url = reverse("api_add_to_cart", kwargs={"id": 123456781, "quantity": 1})
    response = client.post(post_url, {}, content_type="application/json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_add_zero_quantity(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    post_url = reverse("api_add_to_cart", kwargs={"quantity": 0, "id": tv_product.id})
    with pytest.raises(ValidationError):
        client.post(post_url, {}, content_type="application/json")


@pytest.mark.django_db
def test_delete_zero_quantity(tv_product):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    post_url = reverse("api_add_to_cart", kwargs={"quantity": 5, "id": tv_product.id})
    response = client.post(post_url, {}, content_type="application/json")
    item_id = response.data['items'][0]['item_id']
    delete_url = reverse("api_delete_cart_items", kwargs={"quantity": 0, "item_id": item_id})
    with pytest.raises(ValidationError):
        client.delete(delete_url, {}, content_type="application/json")
