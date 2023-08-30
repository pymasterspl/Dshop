import pytest
from django.test import Client
from django.urls import reverse
from lxml import etree

from apps.products_catalogue.models import Category, Product
from apps.products_catalogue.views import ProductListView


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


# tests for creating XML file for Ceneo
@pytest.fixture
def products():
    category = Category.objects.create(name='Test Category', is_active=True)
    return [
        Product.objects.create(name='Telewizor SAMSUNG QE65Q77B 65" QLED 4K 120HZ Tizen TV ', price=3999.00,
                               full_description='Description 1', category=category),
        Product.objects.create(name='Zegarek sportowy GARMIN Venu 2 Plus Biały', price=1739.00,
                               full_description='Description 2', category=category),
    ]


@pytest.mark.django_db
def test_generate_xml_file_for_ceneo(products):
    client = Client()
    response = client.get(reverse('product-list'))

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/xml'
    assert response['Content-Disposition'] == 'attachment; filename="ceneo.xml"'

    root = etree.fromstring(response.content)
    assert root.tag == 'offers'
