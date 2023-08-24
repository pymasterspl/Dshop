import pytest
from apps.products_catalogue.models import Category, Product
from django.urls import reverse

'''
Test todo:
1. simple view - just template?
2. simple view with one product?
2a is the product active?
3. several products - assume 100 products, 9 per page. 
- paginator
- products are active
4. Verify if featured products are first. 
'''
def assert_object_response(response, category):
    context = response.context
    assert response.status_code == 200
    assert len(context.get("object_list")) == 1
    product = context.get("object_list")[0]
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
    Product.objects.create(
        name = "first one",
        category = category,
        price=11,
        short_description="short desc",
        full_description="full_description"
    )
    url = reverse("index")
    # When
    response = client.get(url)
    # Then
    assert_object_response(response, category)




