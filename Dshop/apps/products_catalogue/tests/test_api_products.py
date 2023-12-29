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


@pytest.fixture
def authenticated_api_client(api_client, user_instance_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_instance_token.key}')
    return api_client


@pytest.mark.django_db
def test_access_protected_resource(authenticated_api_client, create_active_product, create_inactive_product):
    url = reverse('products-api-list')
    response = authenticated_api_client.get(url)
    assert response.status_code == 200

    results = response.data.get('results', [])
    assert len(results) == 1

    for product_data in results:
        assert 'id' in product_data
        assert 'category' in product_data
        assert 'name' in product_data
        assert 'price' in product_data
        assert 'short_description' in product_data
        assert 'full_description' in product_data
        assert 'parent_product' in product_data


def test_access_protected_resource_without_authentication(api_client):
    url = reverse('products-api-list')
    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_product_detail(authenticated_api_client, create_active_product):
    url = reverse('products-api-detail', kwargs={'pk': create_active_product.id})
    response = authenticated_api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == create_active_product.id
    assert response.data['name'] == "main product"
    assert response.data['price'] == "11.00"
    assert response.data['short_description'] == "short desc"
    assert response.data['full_description'] == "full_description"


@pytest.mark.django_db
def test_create_product(authenticated_api_client, create_category):
    url = reverse('products-api-list')
    data = {
        'category': create_category.id,  # replace with an existing category ID
        'name': 'Test Product',
        'price': '19.99',
        'short_description': 'Test short description',
        'full_description': 'Test full description',
    }
    response = authenticated_api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['name'] == "Test Product"
    assert response.data['price'] == "19.99"


@pytest.mark.django_db
def test_update_product(authenticated_api_client, create_active_product):
    url = reverse('products-api-detail', kwargs={'pk': create_active_product.id})
    data = {'name': 'Updated product name'}
    response = authenticated_api_client.patch(url, data, format='json')

    assert response.status_code == 200
    assert response.data['name'] == "Updated product name"
    assert response.data['short_description'] == "short desc"
