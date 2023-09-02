import pytest
from apps.products_catalogue.models import Category, Product
from django.urls import reverse

def assert_object_response(response, product, category):
    context = response.context
    assert response.status_code == 200
    product = context.get("product")
    assert product.name == "first one"
    assert product.category == category
    assert product.is_active is True
    assert product.price == 11
    assert product.short_description == "short desc"
    assert product.full_description == "full_description"
    assert "first one" in str(response.content)

@pytest.mark.django_db
def test_single_product_view(client):
    # Given
    category = Category.objects.create(name='Test Category', is_active=True)
    product =Product.objects.create(
        name = "first one",
        category = category,
        price=11,
        short_description="short desc",
        full_description="full_description"
    )
    url = reverse("product-detail", kwargs={'slug': 'first-one', 'id': product.id})
    # When
    response = client.get(url)
    # Then
    assert_object_response(response, product, category)