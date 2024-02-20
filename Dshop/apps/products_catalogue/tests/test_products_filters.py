import pytest

from django.urls import reverse
from Dshop.apps.products_catalogue.models import Product

@pytest.mark.django_db
def test_filter_by_price(client, products):
    # Products is a fixture with 9 products and diff prices.
    # checking ordering
    # Given is in fixture
    # When
    url = reverse("products-list")
    response = client.get(f"{url}?order_by=-price")
    products = response.context["object_list"]
    # Then
    for idx, price in enumerate(range(10, 1, -1)):
        assert products[idx].price == price

@pytest.mark.django_db
def test_product(client, products):
    assert Product.objects.filter(is_active=True).count() == 10

@pytest.mark.django_db
def test_filter_by_price_asc(client, products):
    url = reverse('product-list')
    response = client.get(f'{url}?order_by=price')
    products = response.context['object_list']
    for idx, price in enumerate(range(1, 11)):
        assert products[idx].price == price


@pytest.mark.django_db
def test_filter_by_name(client, products):
    url = reverse('product-list')
    response = client.get(f'{url}?order_by=name')
    products = response.context['object_list']
    for idx, name in enumerate(range(1, 11)):
        assert products[idx].name == f"main product ${idx}"



# @pytest.mark.django_db
# def test_filter_by_name(client, products):
#     url = reverse('product-list')
#     response = client.get(f'{url}?order_by=-name')
#     products = response.context['object_list']
#     for value in range(10, 1, -1):
#         assert products[value].name == f'main product ${value}'




@pytest.mark.django_db
def test_filter_by_created(client, products):
    url = reverse('product-list')
    response = client.get(f'{url}?order_by=created_at')
    products = response.context['object_list']
    for value in range(1, 11):
        assert products[value].name == f'main product ${value}'
