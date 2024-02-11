from rest_framework.test import APIClient
import pytest
from django.urls import reverse


def assert_active_object(data):
    fields_values = {
        "id": 1,
        "category": 1,
        "name": "TV AMOLED",
        "price": "3999.00",
        "short_description": 'Test short description',
        "full_description": 'Test full description',
        "parent_product": None,
    }
    for key, value in data.items():
        assert fields_values[key] == value


@pytest.mark.django_db
def test_get_list_one(api_client, tv_product, inactive_product):
    url = reverse('products-api-list')
    response = api_client.get(url)
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


@pytest.mark.django_db
def test_create_product(api_client_staff, create_category):
    data = {
        'category': create_category.id,
        'name': 'Test Product',
        'price': '19.99',
        'short_description': 'Test short description',
        'full_description': 'Test full description',
    }
    url = reverse('products-api-list')
    response = api_client_staff.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['name'] == "Test Product"
    assert response.data['price'] == "19.99"


@pytest.mark.django_db
def test_update_product(api_client_staff, tv_product):
    url = reverse('products-api-detail', kwargs={'pk': tv_product.id})
    data = {'name': 'Updated product name'}
    response = api_client_staff.patch(url, data, format='json')
    assert response.status_code == 200
    tv_product.refresh_from_db()
    assert tv_product.name == "Updated product name"


@pytest.fixture(autouse=True)
def set_test_pagination_size(settings):
    settings.REST_FRAMEWORK['PAGE_SIZE'] = 5


@pytest.mark.django_db
def test_product_list_empty():
    response = APIClient().get(reverse("products-api-list"))
    print(response.data)
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


@pytest.mark.django_db
def test_product_list_pagination_ten_products_page_too_far(tv_product):
    response = APIClient().get(f"{reverse('products-api-list')}?page=100")
    assert response.status_code == 404