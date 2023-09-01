import pytest
from apps.products_catalogue.models import Category, Product
from django.urls import reverse


def assert_object_response(response, product, category):
    context = response.context
    assert response.status_code == 200
    product = context.get("product")
    assert product.name == "first one"
    assert product.category == category
    assert product.is_active is True
    assert product.price == 11
    assert product.short_description == "short desc"
    assert product.full_description == "full_description"
    assert "first one" in str(response.content)


@pytest.mark.django_db
def test_single_product_view(client):
    # Given
    category = Category.objects.create(name='Test Category', is_active=True)
    product =Product.objects.create(
        name = "first one",
        category = category,
        price=11,
        short_description="short desc",
        full_description="full_description"
    )
    url = reverse("product-detail", kwargs={'slug': 'first-one', 'id': product.id})
    # When
    response = client.get(url)
    # Then
    assert_object_response(response, product, category)
from django.urls import reverse
from lxml import etree

from apps.products_catalogue.models import Category, Product


@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name='Test Category', is_active=True)
    assert category.name == 'Test Category'
    assert category.is_active is True
    assert category.slug is not None


@pytest.mark.django_db
def test_create_category_with_parent():
    parent_category = Category.objects.create(name='Parent Category', is_active=True)
    child_category = Category.objects.create(name='Child Category', is_active=True, parent=parent_category)
    assert child_category.parent == parent_category


@pytest.mark.django_db
def test_generate_xml_file_for_ceneo(client):
    category = Category.objects.create(name='Test Category', is_active=True)

    Product.objects.create(name='Telewizor SAMSUNG QE65Q77B 65" QLED 4K 120HZ Tizen TV ', price=3999.00,
                           full_description='Description 1', category=category)
    Product.objects.create(name='Zegarek sportowy GARMIN Venu 2 Plus Biały', price=1739.00,
                           full_description='Description 2', category=category)

    url = reverse('product-list')
    response = client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/xml'

    root = etree.fromstring(response.content)
    assert root.tag == 'offers'
