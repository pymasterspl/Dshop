import pytest
from django.urls import reverse
from apps.products_catalogue.models import Category, Product
# pylama:ignore=W0404, W0611
from apps.users.conftest import api_client, login_url, login_data, user_instance, user_instance_token


@pytest.fixture
def create_category():
    return Category.objects.create(name='Test Category', is_active=True)


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


@pytest.mark.django_db
def test_access_protected_resource(api_client, user_instance_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')

    url = reverse('products-api-list')
    response = api_client.get(url)
    assert response.status_code == 200


def test_access_protected_resource_without_authentication(api_client):
    url = reverse('products-api-list')
    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_product_detail(api_client, user_instance_token, create_product):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')

    url = reverse('products-api-detail', kwargs={'pk': create_product.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == create_product.id
    assert response.data['name'] == "main product"
    assert response.data['price'] == "11.00"
    assert response.data['short_description'] == "short desc"
    assert response.data['full_description'] == "full_description"


@pytest.mark.django_db
def test_create_product(api_client, user_instance_token, create_category):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')

    url = reverse('products-api-list')
    data = {
        'category': create_category.id,  # replace with an existing category ID
        'name': 'Test Product',
        'price': '19.99',
        'short_description': 'Test short description',
        'full_description': 'Test full description',
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['name'] == "Test Product"
    assert response.data['price'] == "19.99"


@pytest.mark.django_db
def test_update_product(api_client, user_instance_token, create_product):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')

    url = reverse('products-api-detail', kwargs={'pk': create_product.id})
    data = {'name': 'Updated product name'}
    response = api_client.patch(url, data, format='json')

    assert response.status_code == 200
    assert response.data['name'] == "Updated product name"
    assert response.data['short_description'] == "short desc"
