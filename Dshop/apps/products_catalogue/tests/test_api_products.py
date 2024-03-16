from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from django.conf import settings
from apps.products_catalogue.models import ProductImage
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os


@pytest.fixture
def create_product_with_images(tv_product):
    with tempfile.TemporaryDirectory() as temp_dir:
        image_path1 = os.path.join(temp_dir, 'image1.jpg')
        Image.new('RGB', (100, 100)).save(image_path1)
        image1 = SimpleUploadedFile('image1.jpg', open(image_path1, 'rb').read(), content_type='image/jpeg')
        ProductImage.objects.create(product=tv_product, image=image1, is_featured=True)

        image_path2 = os.path.join(temp_dir, 'image2.jpg')
        Image.new('RGB', (150, 150)).save(image_path2)
        image2 = SimpleUploadedFile('image2.jpg', open(image_path2, 'rb').read(), content_type='image/jpeg')
        ProductImage.objects.create(product=tv_product, image=image2, is_featured=False)
    return tv_product


def assert_active_object(data):
    fields_values = {
        "id": 1,
        "category": 1,
        "name": "TV AMOLED",
        "price": "3999.00",
        "short_description": 'Test short description',
        "full_description": 'Test full description',
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
def test_product_detail_with_images(create_product_with_images):
    url = reverse('products-api-detail', kwargs={'pk': create_product_with_images.id})
    response = APIClient().get(url)
    assert response.status_code == 200
    assert_product_with_images(response.data)


@pytest.mark.django_db
def test_get_list_one(tv_product, inactive_product):
    url = reverse('products-api-list')
    response = APIClient().get(url)
    assert response.status_code == 200
    results = response.data.get('results', [])
    assert len(results) == 1
    product_data = results[0]
    assert response.data['count'] == 1
    assert response.data['previous'] is None
    assert response.data['next'] is None
    assert_active_object(product_data)


@pytest.mark.django_db
def test_product_detail_404():
    url = reverse('products-api-detail', kwargs={'pk': 6669})
    response = APIClient().get(url)
    assert response.status_code == 404


def test_pagination_size_in_tests():
    assert settings.REST_FRAMEWORK['PAGE_SIZE'] == 5
    # pagination size changed here: Dshop/Dshop/settings_tests.py


@pytest.mark.django_db
def test_product_list_empty():
    response = APIClient().get(reverse("products-api-list"))
    assert response.status_code == 200
    assert response.data['results'] == []
    assert response.data['count'] == 0
    assert response.data['previous'] is None
    assert response.data['next'] is None


@pytest.mark.django_db
def test_product_detail(tv_product):
    url = reverse('products-api-detail', kwargs={'pk': tv_product.id})
    response = APIClient().get(url)
    assert response.status_code == 200
    assert response.data
    assert_active_object(response.data)



@pytest.mark.django_db
def test_product_list_pagination_ten_products_page_too_far(tv_product):
    response = APIClient().get(f"{reverse('products-api-list')}?page=100")
    assert response.status_code == 404


@pytest.mark.parametrize("page_suffix", ["", "?page=1"])
@pytest.mark.django_db
def test_product_list_pagination_ten_products_page_1(page_suffix, ten_tv_products):
    response = APIClient().get(reverse("products-api-list") + page_suffix)
    results = response.data['results']
    assert len(results) == 5
    assert results[0]['id'] == ten_tv_products[0].id
    assert results[4]['id'] == ten_tv_products[4].id
    assert response.data['count'] == 10
    assert response.data['next'] == "http://testserver/api/products/?page=2"
    assert response.data['previous'] is None
    

@pytest.mark.django_db
def test_product_list_pagination_ten_products_page_2(ten_tv_products):
    response = APIClient().get(f"{reverse('products-api-list')}?page=2")
    results = response.data['results']
    assert response.status_code == 200
    assert len(results) == 5
    assert results[0]['id'] == ten_tv_products[5].id
    assert results[4]['id'] == ten_tv_products[9].id
    assert response.data['count'] == 10
    assert response.data['next'] is None
    assert response.data['previous'] == "http://testserver/api/products/"


@pytest.mark.django_db
def test_product_list_pagination_forty_three_products_page_4(forty_three_tv_products):
    response = APIClient().get(f"{reverse('products-api-list')}?page=4")
    results = response.data['results']
    assert response.status_code == 200
    assert len(results) == 5
    assert results[0]['id'] == forty_three_tv_products[15].id
    assert results[4]['id'] == forty_three_tv_products[19].id
    assert response.data['count'] == 43
    assert response.data['next'] == "http://testserver/api/products/?page=5"
    assert response.data['previous'] == "http://testserver/api/products/?page=3"


@pytest.mark.django_db
def test_product_list_pagination_forty_three_products_page_9(forty_three_tv_products):
    response = APIClient().get(f"{reverse('products-api-list')}?page=9")
    results = response.data['results']
    assert response.status_code == 200
    assert len(results) == 3
    assert results[0]['id'] == forty_three_tv_products[40].id
    assert results[2]['id'] == forty_three_tv_products[42].id
    assert response.data['count'] == 43
    assert response.data['next'] is None
    assert response.data['previous'] == "http://testserver/api/products/?page=8"


@pytest.mark.django_db
def test_delete_unallowed_method(tv_product):
    response = APIClient().delete(reverse('products-api-detail', kwargs={'pk': tv_product.pk}))
    assert response.status_code == 405