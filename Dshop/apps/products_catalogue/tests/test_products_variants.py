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
    child1 = Product.objects.create(
        name="child product 1",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description",
        parent_product=main_product
    )
    child2 = Product.objects.create(
        name="child product 2",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description",
        parent_product=main_product
    )
    assert Product.objects.count() == 3
    assert main_product.product_set.count() == 2
    assert child1.parent_product == main_product
    assert child2.parent_product == main_product


@pytest.mark.django_db
def test_product_variant_attributes():
    category = Category.objects.create(name='Test Category', is_active=True)
    main_product = Product.objects.create(
        name='main_product',
        category=category,
        price=10,
        short_description='short desc',
        full_description="full desc",
    )
    variant1 = Product.objects.create(
        name="child product 1",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description",
        parent_product=main_product
    )
    ProductAttribute.objects.create(
        product=variant1,
        key='color',
        value='red'
    )
    ProductAttribute.objects.create(
        product=variant1,
        key='size',
        value='XL'
    )
    assert variant1.get_attributes().count() == 2
