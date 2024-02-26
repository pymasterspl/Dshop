from decimal import Decimal

import pytest

from django.urls import reverse
from ..models import Product


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
    url = reverse("products-list")
    response = client.get(f"{url}?order_by=price")
    products = response.context['object_list']
    for idx, price in enumerate(range(1, 11)):
        assert products[idx].price == price


@pytest.mark.django_db
def test_filter_by_price_desc(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?order_by=-price")
    products = response.context['object_list']
    for idx, price in enumerate(range(10, 0, -1)):
        assert products[idx].price == Decimal(price)


@pytest.mark.django_db
def test_filter_by_name(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?order_by=name")
    products = response.context['object_list']
    for idx, name in enumerate([1, 10, 2, 3, 4, 5, 6, 7, 8, 9]):
        assert products[idx].name == f"main product ${name}"


@pytest.mark.django_db
def test_filter_by_name_desc(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?order_by=-name")
    products = response.context['object_list']
    for idx, name in enumerate([9, 8, 7, 6, 5, 4, 3, 2, 10, 1]):
        assert products[idx].name == f'main product ${name}'


@pytest.mark.django_db
def test_filter_by_created(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?order_by=created_at")
    products = response.context['object_list']
    for idx, value in enumerate(range(1, 10)):
        assert products[idx].created_at <= products[idx + 1].created_at


@pytest.mark.django_db
def test_filter_by_created_desc(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?order_by=-created_at")
    products = response.context['object_list']
    for idx, value in enumerate(range(10, 1, -1)):
        assert products[idx].created_at >= products[idx + 1].created_at


@pytest.mark.django_db
def test_filter_category(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?category_name=Test_Category")
    products = response.context['object_list']
    for idx, value in enumerate(range(1, 11)):
        assert products[idx].category.name == 'Test Category'


@pytest.mark.django_db
def test_filter_by_min_price(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?prince__gt=5")
    products = response.context['object_list']
    for value in range(5, 10):
        assert products[value].price == Decimal(value + 1)


@pytest.mark.django_db
def test_filter_by_max_price(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?prince__lt=5")
    products = response.context['object_list']
    for idx, value in enumerate(range(5)):
        assert products[idx].price == Decimal(value + 1)


@pytest.mark.django_db
def test_filter_by_name(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?name=main+product+$10")
    products = response.context['object_list']
    assert products[0].name == 'main product $10'

@pytest.mark.django_db
def test_filter_availability(client, products):
    url = reverse("products-list")
    response = client.get(f"{url}?availability=3")
    products = response.context['object_list']
    for idx, value in enumerate(range(1, 11)):
        assert products[idx].availability == 3