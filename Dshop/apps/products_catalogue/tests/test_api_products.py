import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.products_catalogue.models import Category, Product


@pytest.fixture
def create_active_product():
    category = Category.objects.create(name='Test Category', is_active=True)
    return Product.objects.create(
        name="main product",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description",
        is_active=True
    )


@pytest.fixture
def create_inactive_product():
    category = Category.objects.create(name='Test Category 2', is_active=True)
    return Product.objects.create(
        name="main product inactive",
        category=category,
        price=150,
        short_description="short desc inactive",
        full_description="full_description inactive",
        is_active=False
    )


def assert_active_object(data):
    assert data['category'] is not None

    fields_values = {
        "id": 1,
        "category": 1,
        "name": "main product",
        "price": "11.00",
        "short_description": "short desc",
        "full_description": "full_description",
        "parent_product": None,
    }
    for key, value in data.items():
        assert fields_values[key] == value


@pytest.mark.django_db
def test_access_protected_resource(api_client_authed, create_active_product, create_inactive_product):
    url = reverse('products-api-list')
    response = api_client_authed.get(url)
    assert response.status_code == 200

    results = response.data.get('results', [])
    assert len(results) == 1

    product_data = results[0]

    assert_active_object(product_data)


@pytest.mark.django_db
def test_product_detail(api_client_authed, create_active_product):
    url = reverse('products-api-detail', kwargs={'pk': create_active_product.id})
    response = api_client_authed.get(url)

    assert response.status_code == 200
    assert response.data['id'] == create_active_product.id
    assert response.data['name'] == "main product"
    assert response.data['price'] == "11.00"
    assert response.data['short_description'] == "short desc"
    assert response.data['full_description'] == "full_description"


@pytest.mark.django_db
def test_create_product(api_client_authed, create_category):
    url = reverse('products-api-list')
    data = {
        'category': create_category.id,
        'name': 'Test Product',
        'price': '19.99',
        'short_description': 'Test short description',
        'full_description': 'Test full description',
    }
    response = api_client_authed.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['name'] == "Test Product"
    assert response.data['price'] == "19.99"


@pytest.mark.django_db
def test_update_product(api_client_authed, create_active_product):
    url = reverse('products-api-detail', kwargs={'pk': create_active_product.id})
    data = {'name': 'Updated product name'}
    response = api_client_authed.patch(url, data, format='json')

    assert response.status_code == 200
    assert response.data['name'] == "Updated product name"
    assert response.data['short_description'] == "short desc"
