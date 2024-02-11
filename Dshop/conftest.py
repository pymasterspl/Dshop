import pytest
from dj_shop_cart.cart import get_cart_class
from django.urls import reverse
from pytest import fixture
from apps.products_catalogue.models import Category, Product
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


User = get_user_model()
Cart = get_cart_class()


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def api_client_authed():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user)
    return client

@pytest.fixture
def api_client_staff():
    client = APIClient()
    staff_user = User.objects.create_user(username='staffuser', is_staff=True, password="staffsword")
    client.force_authenticate(staff_user)
    return client

@pytest.fixture
def api_client_admin():
    client = APIClient()
    admin = User.objects.create_user(username='admin', is_staff=True, is_admin=True, password='@dmin123')
    client.force_authenticate(admin)
    return client

@pytest.fixture
def create_category():
    return Category.objects.create(name='Test Category', is_active=True)

@fixture
@pytest.mark.django_db
def tv_product():
    category = Category.objects.create(
        name='Test Category',
        is_active=True
    )
    product = Product.objects.create(
        name='TV AMOLED',
        price=3999.00,
        full_description='Test full description',
        short_description='Test short description',
        category=category,
    )
    return product


@pytest.fixture
def inactive_product():
    category = Category.objects.create(name='Test Category 2', is_active=True)
    return Product.objects.create(
        name="main product inactive",
        category=category,
        price=150,
        short_description="short desc inactive",
        full_description="full_description inactive",
        is_active=False
    )


@fixture
@pytest.mark.django_db
def ten_tv_products():
    category = Category.objects.create(
        name='TVs',
        is_active=True
    )
    tv_data = [
        {'name': 'TV AMOLED 32"', 'price': 599.00, 'full_description': 'High-quality 32-inch AMOLED TV.', 'category': category},
        {'name': 'Smart TV 40"', 'price': 899.00, 'full_description': '40-inch Smart TV with advanced features.', 'category': category},
        {'name': '4K Ultra HD TV 55"', 'price': 1299.00, 'full_description': '55-inch 4K Ultra HD TV for stunning visuals.', 'category': category},
        {'name': 'Curved TV 65"', 'price': 1999.00, 'full_description': 'Immersive 65-inch curved TV experience.', 'category': category},
        {'name': 'OLED TV 50"', 'price': 1699.00, 'full_description': '50-inch OLED TV with vibrant colors.', 'category': category},
        {'name': 'QLED TV 75"', 'price': 2999.00, 'full_description': '75-inch QLED TV for a cinematic viewing experience.', 'category': category},
        {'name': 'Android TV 43"', 'price': 799.00, 'full_description': '43-inch Android TV with a wide range of apps.', 'category': category},
        {'name': 'HD LED TV 24"', 'price': 299.00, 'full_description': '24-inch HD LED TV for compact spaces.', 'category': category},
        {'name': 'Outdoor TV 55"', 'price': 2499.00, 'full_description': '55-inch Outdoor TV for outdoor entertainment.', 'category': category},
        {'name': 'Gaming TV 50"', 'price': 1799.00, 'full_description': '50-inch Gaming TV with low input lag.', 'category': category},
    ]
    return [Product.objects.create(**data) for data in tv_data]


@fixture
@pytest.mark.django_db
def edifier_product():
    category = Category.objects.create(
        name='Test Category',
        is_active=True
    )
    product = Product.objects.create(
        name='Edifier r1700dbs',
        price=499.00,
        full_description='Description 2',
        category=category
    )
    return product


@fixture
def fake_cart_detail_view_request(client):
    url = reverse(
        "cart_detail"
    )
    fake_response = client.get(url)
    fake_request = fake_response.wsgi_request

    return fake_request


@fixture
def fake_add_to_cart_view_request(client, tv_product):
    url = reverse(
        'add_to_cart',
        kwargs={
            'slug': tv_product.slug,
            'id': tv_product.id,
            'quantity': 1
        }
    )
    fake_response = client.post(url)
    fake_add_request = fake_response.wsgi_request

    return fake_add_request
