from decimal import Decimal
import pytest
from apps.products_catalogue.models import Category, Product


@pytest.fixture
def products():
    category = Category.objects.create(name='Test Category', is_active=True)
    products = []
    for idx in range(1, 11):
        prod = Product.objects.create(
                name=f"main product ${idx}",
                category=category,
                price=idx,
                short_description="short desc inactive",
                full_description="full_description inactive",
                is_active=True,
                created_at=True,
                availability=3,
            )
        products.append(prod)
    return products


def expected_prod_set(prods):
    return {(obj.id, obj.name, Decimal(obj.price), obj.category.id) for obj in prods}

def api_prod_set(response):
    return {(el["id"], el["name"], Decimal(el["price"]), el["category"]) for el in response.data["results"]}