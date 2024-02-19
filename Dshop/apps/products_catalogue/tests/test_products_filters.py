import pytest


from django.urls import reverse

from apps.products_catalogue.models import Product


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
    for idx, price in enumerate(range (10, 1, -1)):
        assert products[idx].price == price

