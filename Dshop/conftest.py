import datetime
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
def api_client_authenticated():
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
        {'name': 'TV AMOLED 32"', 'price': 599.00, 'full_description': 'High-quality 32-inch AMOLED TV.', 'category': category, 'availability': 1},
        {'name': 'Smart TV 40"', 'price': 899.00, 'full_description': '40-inch Smart TV with advanced features.', 'category': category, 'availability': 3},
        {'name': '4K Ultra HD TV 55"', 'price': 1299.00, 'full_description': '55-inch 4K Ultra HD TV for stunning visuals.', 'category': category, 'availability': 7},
        {'name': 'Curved TV 65"', 'price': 1999.00, 'full_description': 'Immersive 65-inch curved TV experience.', 'category': category, 'availability': 14},
        {'name': 'OLED TV 50"', 'price': 1699.00, 'full_description': '50-inch OLED TV with vibrant colors.', 'category': category, 'availability': 90},
        {'name': 'QLED TV 75"', 'price': 2999.00, 'full_description': '75-inch QLED TV for a cinematic viewing experience.', 'category': category, 'availability': 99},
        {'name': 'Android TV 43"', 'price': 799.00, 'full_description': '43-inch Android TV with a wide range of apps.', 'category': category, 'availability': 110},
        {'name': 'HD LED TV 24"', 'price': 299.00, 'full_description': '24-inch HD LED TV for compact spaces.', 'category': category, 'availability': 99},
        {'name': 'Outdoor TV 55"', 'price': 2499.00, 'full_description': '55-inch Outdoor TV for outdoor entertainment.', 'category': category, 'availability': 99},
        {'name': 'Gaming TV 50"', 'price': 1799.00, 'full_description': '50-inch Gaming TV with low input lag.', 'category': category, 'availability': 99},
    ]
    result = []
    for idx, tv in enumerate(tv_data):
        tv['created_at'] = datetime.datetime.now() - datetime.timedelta(days=idx)
        result.append(Product.objects.create(**tv))
    return result
@fixture
@pytest.mark.django_db
def forty_three_tv_products():
    category, _ = Category.objects.get_or_create(
        name='TVs',
        is_active=True
    )
    tv_data = [
        {'name': 'LED TV 22', 'price': 349.00, 'full_description': '22-inch LED TV for small spaces.', 'category': category},
        {'name': 'Smart TV 50', 'price': 1499.00, 'full_description': '50-inch Smart TV with voice control.', 'category': category},
        {'name': 'Ultra Slim TV 32', 'price': 699.00, 'full_description': '32-inch Ultra Slim TV for a sleek look.', 'category': category},
        {'name': 'Portable TV 15', 'price': 199.00, 'full_description': '15-inch Portable TV for on-the-go entertainment.', 'category': category},
        {'name': 'HD Ready TV 28', 'price': 449.00, 'full_description': '28-inch HD Ready TV for clear visuals.', 'category': category},
        {'name': 'Smart LED TV 65', 'price': 2499.00, 'full_description': '65-inch Smart LED TV with streaming apps.', 'category': category},
        {'name': 'Curved OLED TV 55', 'price': 1899.00, 'full_description': '55-inch Curved OLED TV for immersive viewing.', 'category': category},
        {'name': '4K QLED TV 85', 'price': 3999.00, 'full_description': '85-inch 4K QLED TV for a cinematic experience.', 'category': category},
        {'name': 'Portable Gaming TV 20', 'price': 299.00, 'full_description': '20-inch Portable Gaming TV for gaming on the move.', 'category': category},
        {'name': 'Outdoor Smart TV 65', 'price': 2799.00, 'full_description': '65-inch Outdoor Smart TV for outdoor entertainment.', 'category': category},
        {'name': 'Ultra HD Smart TV 60', 'price': 2199.00, 'full_description': '60-inch Ultra HD Smart TV with advanced features.', 'category': category},
        {'name': 'Portable LED TV 18', 'price': 179.00, 'full_description': '18-inch Portable LED TV for convenient viewing.', 'category': category},
        {'name': 'QLED Gaming TV 40', 'price': 1299.00, 'full_description': '40-inch QLED Gaming TV with low input lag.', 'category': category},
        {'name': 'Android Smart TV 55', 'price': 1699.00, 'full_description': '55-inch Android Smart TV for a connected experience.', 'category': category},
        {'name': 'Curved 4K OLED TV 70', 'price': 2899.00, 'full_description': '70-inch Curved 4K OLED TV for stunning visuals.', 'category': category},
        {'name': 'HD Outdoor TV 32', 'price': 599.00, 'full_description': '32-inch HD Outdoor TV for outdoor entertainment.', 'category': category},
        {'name': 'Slim LED TV 26', 'price': 399.00, 'full_description': '26-inch Slim LED TV for a space-saving design.', 'category': category},
        {'name': 'Smart QLED TV 50', 'price': 1599.00, 'full_description': '50-inch Smart QLED TV with voice recognition.', 'category': category},
        {'name': 'Portable HD TV 14', 'price': 149.00, 'full_description': '14-inch Portable HD TV for on-the-go use.', 'category': category},
        {'name': 'Gaming Monitor TV 27', 'price': 699.00, 'full_description': '27-inch Gaming Monitor TV for console gaming.', 'category': category},
        {"name": "Ultra HD Smart TV 61", "price": 2299.00, "full_description": "61-inch Ultra HD Smart TV with advanced features.", "category": category},
        {"name": "Portable LED TV 19", "price": 189.00, "full_description": "19-inch Portable LED TV for convenient viewing.", "category": category},
        {"name": "QLED Gaming TV 41", "price": 1399.00, "full_description": "41-inch QLED Gaming TV with low input lag.", "category": category},
        {"name": "Android Smart TV 56", "price": 1799.00, "full_description": "56-inch Android Smart TV for a connected experience.", "category": category},
        {"name": "Curved 4K OLED TV 71", "price": 2999.00, "full_description": "71-inch Curved 4K OLED TV for stunning visuals.", "category": category},
        {"name": "HD Outdoor TV 33", "price": 699.00, "full_description": "33-inch HD Outdoor TV for outdoor entertainment.", "category": category},
        {"name": "Slim LED TV 27", "price": 499.00, "full_description": "27-inch Slim LED TV for a space-saving design.", "category": category},
        {"name": "Smart QLED TV 51", "price": 1699.00, "full_description": "51-inch Smart QLED TV with voice recognition.", "category": category},
        {"name": "Portable HD TV 15", "price": 159.00, "full_description": "15-inch Portable HD TV for on-the-go use.", "category": category},
        {"name": "Gaming Monitor TV 28", "price": 799.00, "full_description": "28-inch Gaming Monitor TV for console gaming.", "category": category},
        {"name": "Ultra HD Smart TV 62", "price": 2399.00, "full_description": "62-inch Ultra HD Smart TV with advanced features.", "category": category},
        {"name": "Portable LED TV 20", "price": 199.00, "full_description": "20-inch Portable LED TV for convenient viewing.", "category": category},
        {"name": "QLED Gaming TV 42", "price": 1499.00, "full_description": "42-inch QLED Gaming TV with low input lag.", "category": category},
        {"name": "Android Smart TV 57", "price": 1899.00, "full_description": "57-inch Android Smart TV for a connected experience.", "category": category},
        {"name": "Curved 4K OLED TV 72", "price": 3099.00, "full_description": "72-inch Curved 4K OLED TV for stunning visuals.", "category": category},
        {"name": "HD Outdoor TV 34", "price": 799.00, "full_description": "34-inch HD Outdoor TV for outdoor entertainment.", "category": category},
        {"name": "Slim LED TV 28", "price": 549.00, "full_description": "28-inch Slim LED TV for a space-saving design.", "category": category},
        {"name": "Smart QLED TV 52", "price": 1799.00, "full_description": "52-inch Smart QLED TV with voice recognition.", "category": category},
        {"name": "Portable HD TV 16", "price": 169.00, "full_description": "16-inch Portable HD TV for on-the-go use.", "category": category},
        {"name": "Gaming Monitor TV 29", "price": 899.00, "full_description": "29-inch Gaming Monitor TV for console gaming.", "category": category},
        {"name": "Ultra HD Smart TV 63", "price": 2499.00, "full_description": "63-inch Ultra HD Smart TV with advanced features.", "category": category},
        {"name": "Portable LED TV 21", "price": 209.00, "full_description": "21-inch Portable LED TV for convenient viewing.", "category": category},
        {"name": "4K UHD OLED TV 85", "price": 4999.00, "full_description": "85-inch 4K UHD OLED TV for breathtaking visuals.", "category": category}
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
