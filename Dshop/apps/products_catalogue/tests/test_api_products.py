from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from django.conf import settings


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
def test_get_list_one(set_test_pagination_size, tv_product, inactive_product):
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


@pytest.fixture
def set_test_pagination_size(settings, autouse=True):
    settings.REST_FRAMEWORK['PAGE_SIZE'] = 5


def test_pagination_size_in_tests():
    assert settings.REST_FRAMEWORK['PAGE_SIZE'] == 5
    # pagination size changed here: Dshop/Dshop/settings_tests.py

@pytest.mark.django_db
def test_product_list_empty(set_test_pagination_size):
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



@pytest.mark.django_db
def test_product_list_pagination_ten_products_page_too_far(set_test_pagination_size, tv_product):
    response = APIClient().get(f"{reverse('products-api-list')}?page=100")
    assert response.status_code == 404


@pytest.mark.parametrize("page_suffix", ["", "?page=1"])
@pytest.mark.django_db
def test_product_list_pagination_ten_products_page_1(set_test_pagination_size, page_suffix, ten_tv_products):#, ten_tv_products):
    response = APIClient().get(reverse("products-api-list") + page_suffix)
    results = response.data['results']
    assert len(results) == 5
    assert results[0]['id'] == ten_tv_products[0].id
    assert results[4]['id'] == ten_tv_products[4].id
    assert response.data['count'] == 10
    assert response.data['next'] == "http://testserver/api/products/?page=2"
    assert response.data['previous'] is None
    

@pytest.mark.django_db
def test_product_list_pagination_ten_products_page_2(set_test_pagination_size, ten_tv_products):
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
def test_product_list_pagination_forty_three_products_page_4(set_test_pagination_size, forty_three_tv_products):
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
def test_product_list_pagination_forty_three_products_page_9(set_test_pagination_size, forty_three_tv_products):
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