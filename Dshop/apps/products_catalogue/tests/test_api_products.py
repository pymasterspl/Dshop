import pytest
from django.urls import reverse
from apps.products_catalogue.models import Category, Product, ProductImage
# pylama:ignore=W0404, W0611
from apps.users.conftest import api_client, login_url, login_data, user_instance, user_instance_token
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os

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


@pytest.fixture
def create_product_with_images(create_category):
    product = Product.objects.create(
        name="Product with images",
        category=create_category,
        price=29.99,
        short_description="Product short description",
        full_description="Product full description",
        is_active=True
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        image_path1 = os.path.join(temp_dir, 'image1.jpg')
        Image.new('RGB', (100, 100)).save(image_path1)
        image1 = SimpleUploadedFile('image1.jpg', open(image_path1, 'rb').read(), content_type='image/jpeg')
        ProductImage.objects.create(product=product, image=image1, is_featured=True)

        image_path2 = os.path.join(temp_dir, 'image2.jpg')
        Image.new('RGB', (150, 150)).save(image_path2)
        image2 = SimpleUploadedFile('image2.jpg', open(image_path2, 'rb').read(), content_type='image/jpeg')
        ProductImage.objects.create(product=product, image=image2, is_featured=False)
    return product


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
        "images": []
    }
    for key, value in data.items():
        assert fields_values[key] == value


def assert_product_with_images(data):
    assert 'images' in data
    assert len(data['images']) == 2
    expected_image_data1 = {
        "image": data['images'][0]['image'],
    }
    expected_image_data2 = {
        "image": data['images'][1]['image'],
    }
    assert expected_image_data1 in data['images']
    assert expected_image_data2 in data['images']


@pytest.mark.django_db
def test_product_detail_with_images(authenticated_api_client, create_product_with_images):
    url = reverse('products-api-detail', kwargs={'pk': create_product_with_images.id})
    response = authenticated_api_client.get(url)

    assert response.status_code == 200
    assert_product_with_images(response.data)


@pytest.mark.django_db
def test_access_protected_resource(authenticated_api_client, create_active_product, create_inactive_product):
    url = reverse('products-api-list')
    response = authenticated_api_client.get(url)
    assert response.status_code == 200

    results = response.data.get('results', [])
    assert len(results) == 1

    product_data = results[0]

    assert_active_object(product_data)


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
        'category': create_category.id,
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
