import pytest
from decimal import Decimal
from freezegun import freeze_time
from apps.products_catalogue.models import Category, Product, ProductAttribute


@pytest.fixture
def create_product_with_category():
    category = Category.objects.create(name='Test Category', is_active=True)
    return Product.objects.create(
        name="main product",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description"
    )


@pytest.mark.django_db
def test_product_creation_with_variants():
    category = Category.objects.create(name='Test Category', is_active=True)
    main_product = Product.objects.create(
        name='main_product',
        category=category,
        price=10,
        short_description='short desc',
        full_description="full desc",
    )
    Product.objects.create(
        name="child product 1",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description",
        parent_product=main_product
    )
    Product.objects.create(
        name="child product 2",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description",
        parent_product=main_product
    )
    assert Product.objects.count() == 3
