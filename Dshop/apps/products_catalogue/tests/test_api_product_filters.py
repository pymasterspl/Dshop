from decimal import Decimal
from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from apps.products_catalogue.tests.conftest import api_prod_set, expected_prod_set
from apps.products_catalogue.models import Category


URL = reverse("products-api-list")
pytestmark = pytest.mark.django_db


@pytest.fixture
def named_products(products):
    products[0].name = "J"
    products[1].name = "A"
    products[2].name = "B"
    products[3].name = "I"
    products[4].name = "G"
    products[5].name = "C"
    products[6].name = "F"
    products[7].name = "H"
    products[8].name = "E"
    products[9].name = "D"
    products[0].save()
    products[1].save()
    products[2].save()
    products[3].save()
    products[4].save()
    products[5].save()
    products[6].save()
    products[7].save()
    products[8].save()
    products[9].save()
    return products

def test_products_api_order_by_price_asc(products):
    response = APIClient().get(f"{URL}?order_by=price")
    products_data = response.data["results"]
    print(response.data)
    assert response.status_code == 200
    assert response.data["count"] == 10
    for value, prod in enumerate(products_data, start=1):
        assert Decimal(prod["price"]) == Decimal(value)

def test_products_api_order_by_price_desc(products):
    response = APIClient().get(f"{URL}?order_by=-price")
    products_data = response.data["results"]
    assert response.status_code == 200
    assert response.data["count"] == 10
    for value, prod in zip(range(10, 5, -1), products_data):
        assert Decimal(prod["price"]) == Decimal(value)

def test_products_api_filter_by_name(products):
    response = APIClient().get(f"{URL}?name=main+product+$10")
    products_data = response.data["results"]
    assert response.status_code == 200
    assert len(products_data) == 1
    assert products_data[0]["name"] == "main product $10"

def test_products_api_filter_by_price(products):
    PRICE = 10
    response = APIClient().get(f"{URL}?price={PRICE}")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert Decimal(response.data["results"][0]["price"]) == PRICE
    assert response.data["results"][0]["name"] == "main product $10"

@pytest.mark.parametrize("availability, other_availability", [
    (1, 99),
    (3, 99),
    (7, 99),
    (14, 99),
    (90, 99),
    (99, 1),
    (110, 99)
])
def test_products_api_filter_by_availability(products, availability, other_availability):
    for prod in products[5:]:
        prod.availability = other_availability
        prod.save()
    remaining_products = products[:5]
    for prod in remaining_products:
        prod.availability = availability
        prod.save()
    response = APIClient().get(f"{URL}?availability={availability}")
    expected_result = expected_prod_set(remaining_products)
    api_results = api_prod_set(response)
    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    assert expected_result == api_results

@pytest.mark.parametrize("availability, expected_count", [
    (1, 2),
    (3, 4),
    (7, 7),
    (14, 10),
])
def test_products_api_filters_by_availability_days(products, availability, expected_count):
    products[0].availability = 1
    products[1].availability = 1
    products[2].availability = 3
    products[3].availability = 3
    products[4].availability = 7
    products[5].availability = 7
    products[6].availability = 7
    products[7].availability = 14
    products[8].availability = 14
    products[9].availability = 14
    for prod in products:
        prod.save()
    response = APIClient().get(f"{URL}?availability={availability}")
    assert response.status_code == 200
    assert response.data["count"] == expected_count

def test_products_api_filters_availability_by_category(products, api_client):
    other_cat = Category.objects.create(name="Test Category 2")
    for prod in products[5:]:
        prod.category = other_cat
        prod.save()
    response_1 = api_client.get(f"{URL}?category_name=Test+Category")
    response_2 = api_client.get(f"{URL}?category_name=Test+Category+2")
    api_result_1 = api_prod_set(response_1)
    api_result_2 = api_prod_set(response_2)
    expected_result_1 = expected_prod_set(products[:5])
    expected_result_2 = expected_prod_set(products[5:])
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert len(response_1.data["results"]) == 5
    assert len(response_2.data["results"]) == 5
    assert response_1.data["count"] == 5
    assert response_2.data["count"] == 5
    assert api_result_1 == expected_result_1
    assert api_result_2 == expected_result_2

def test_products_api_filters_price_lt(products):
    MAX_PRICE = Decimal("5.5")
    expected_results = expected_prod_set(products[:5])
    response = APIClient().get(f"{URL}?price__lt={MAX_PRICE}")
    api_results = api_prod_set(response)
    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    assert api_results == expected_results

def test_products_api_filters_price_gt(products):
    MIN_PRICE = Decimal("5.5")
    expected_results = expected_prod_set(products[5:])
    response = APIClient().get(f"{URL}?price__gt={MIN_PRICE}")
    api_results = api_prod_set(response)
    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    assert api_results == expected_results

def test_products_api_order_by_name_asc(named_products):
    response = APIClient().get(f"{URL}?order_by=name")
    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    for name, el in zip("ABCDE", response.data["results"]):
        assert name == el["name"]

def test_products_api_order_by_name_desc(named_products):
    response = APIClient().get(f"{URL}?order_by=-name")
    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    for name, el in zip("JIHGF", response.data["results"]):
        assert name == el["name"]

def test_products_api_oder_by_created_at_desc(products):
    response = APIClient().get(f"{URL}?order_by=-created_at")
    expected_results = [products[9], products[8], products[7], products[6], products[5]]
    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    for obj, el in zip(expected_results, response.data["results"]):
        assert obj.id == el["id"]
        assert obj.name == el["name"]
        assert Decimal(obj.price) == Decimal(el["price"])
        assert obj.category.id == el["category"]

def test_products_api_oder_by_created_at_asc(products):
    response = APIClient().get(f"{URL}?order_by=created_at")
    expected_results = products[:5]
    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    for obj, el in zip(expected_results, response.data["results"]):
        assert obj.id == el["id"]
        assert obj.name == el["name"]
        assert Decimal(obj.price) == Decimal(el["price"])
        assert obj.category.id == el["category"]