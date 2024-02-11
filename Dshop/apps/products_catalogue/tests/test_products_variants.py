import pytest
from apps.products_catalogue.models import Category, Product
from django.urls import reverse


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


def assert_object_product_response(response, category):
    context = response.context
    assert response.status_code == 200
    product = context.get("product")
    products_variants = context.get("product_variants")
    assert product.name == "main_product"
    assert products_variants[0].name == "child product 1"
    assert products_variants[1].name == "child product 2"
    assert products_variants[0].category == category
    assert products_variants[1].is_active is True
    assert products_variants[0].price == 11


@pytest.mark.django_db
def test_product_detail_view(client):
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
    url = reverse("product-detail", kwargs={'slug': 'main_product', 'id': main_product.id})
    response = client.get(url)
    assert_object_product_response(response, category)


def assert_object_category_response(response, category):
    context = response.context
    assert response.status_code == 200
    products_in_category = context.get("products")
    assert products_in_category.count() == 1
    assert products_in_category.first().name == 'main_product_2'
    assert products_in_category.first().price == 10
    assert products_in_category.first().category == category
    assert products_in_category.first().category.name == 'Test Category'


@pytest.mark.django_db
def test_category_detail_view(client):
    category = Category.objects.create(name='Test Category', is_active=True)
    Product.objects.create(
        name='main_product_1',
        category=category,
        price=10,
        short_description='short desc',
        full_description="full desc",
        is_active=False
    )
    main_product = Product.objects.create(
        name='main_product_2',
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
    url = reverse("category-detail", kwargs={'slug': 'test-category', 'id': category.id})
    response = client.get(url)
    assert_object_category_response(response, category)
