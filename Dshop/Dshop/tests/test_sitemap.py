import pytest
from django.urls import reverse
import xml.etree.ElementTree as ET
from apps.products_catalogue.models import Category, Product
from decimal import Decimal


CURRENT_DOMAIN = "http://example.com"


def xml_contains_texts(element, *texts):
    dict_ = {text: False for text in texts}
    for xml_text in element.itertext():
        if xml_text in dict_:
            dict_[xml_text] = True
    print(f"{dict_.values()}")
    return all(dict_.values())


def test_xml_contains_text_1():
    xml = """
    <tag>
        <el>one</el>
        <el>two</el>
        <el>three</el>
        <el>four</el>
        <el>five</el>
    </tag>"""
    root = ET.fromstring(xml)
    assert xml_contains_texts(root, 'one', 'two', 'three', 'four', 'five') is True


def test_xml_contains_text_2():
    xml = """
    <tag>
        <el>one</el>
        <el>two</el>
        <el>three</el>
        <el>four</el>
        <el>five</el>
    </tag>"""
    root = ET.fromstring(xml)
    assert xml_contains_texts(root, 'xxx') is False


def test_xml_contains_text_3():
    xml = """
    <tag>
        <el>one</el>
        <el>two</el>
        <el>three</el>
        <el>four</el>
        <el>five</el>
    </tag>"""
    root = ET.fromstring(xml)
    assert xml_contains_texts(root, 'one', 'three', 'five') is True


def test_xml_contains_text_4():
    xml = """
    <tag>
        <el>one</el>
        <el>two</el>
        <el>three</el>
        <el>four</el>
        <el>five</el>
    </tag>"""
    root = ET.fromstring(xml)
    assert xml_contains_texts(root, 'one', 'xxx') is False


def test_xml_contains_text_5():
    xml = """
    <tag>
        <el>one</el>
        <el>two</el>
        <el>three</el>
        <el>four</el>
        <el>five</el>
    </tag>"""
    root = ET.fromstring(xml)
    assert xml_contains_texts(root, 'one', 'two', 'three', 'four', 'five', 'six') is False


def test_xml_contains_text_6():
    xml = """
    <tag>
        <el>one</el>
        <el>two</el>
        <el>three</el>
        <el>four</el>
        <el>five</el>
    </tag>"""
    root = ET.fromstring(xml)
    assert xml_contains_texts(root, 'one') is True

def test_xml_contains_text_7():
    xml = """
    <tag1>
        <tag2>
            <tag3>text</tag3>
        </tag2>
    </tag1>
    """
    root = ET.fromstring(xml)
    assert xml_contains_texts(root, "text") is True

@pytest.mark.django_db
def test_is_xml(client):
    url = reverse("django.contrib.sitemaps.views.sitemap")
    response = client.get(url)
    assert response.status_code == 200
    xml = response.content

    root = ET.fromstring(xml.decode())
    assert ET.iselement(root)


@pytest.mark.django_db
def test_product_in_xml(client):
    category = Category.objects.create(name="Obuwie")
    product_1 = Product.objects.create(
        category=category,
        name="Trampki",
        price=Decimal(20),
        short_description="Tanie dobre buty",
        full_description="Tanie dobre buty. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    product_url = CURRENT_DOMAIN + product_1.get_absolute_url()

    print(f"{product_url=}")

    url = reverse("django.contrib.sitemaps.views.sitemap")
    response = client.get(url)
    assert response.status_code == 200
    xml = response.content
    root = ET.fromstring(xml.decode())

    assert xml_contains_texts(root, product_url) is True



@pytest.mark.django_db
def test_three_products_in_xml(client):
    category = Category.objects.create(name="Obuwie")
    product_1 = Product.objects.create(
        category=category,
        name="Trampki",
        price=Decimal(20),
        short_description="Tanie dobre buty",
        full_description="Tanie dobre buty. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    product_2 = Product.objects.create(
        category=category,
        name="Sandały",
        price=Decimal(100),
        short_description="Tanie dobre sandały",
        full_description="Tanie dobre sandały. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    product_3 = Product.objects.create(
        category=category,
        name="Adidasy",
        price=Decimal(300),
        short_description="Tanie dobre adidast",
        full_description="Tanie dobre adidast. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    product_1_url = CURRENT_DOMAIN + product_1.get_absolute_url()
    product_2_url = CURRENT_DOMAIN + product_2.get_absolute_url()
    product_3_url = CURRENT_DOMAIN + product_3.get_absolute_url()

    url = reverse("django.contrib.sitemaps.views.sitemap")
    response = client.get(url)
    assert response.status_code == 200
    xml = response.content
    root = ET.fromstring(xml.decode())

    assert xml_contains_texts(root, product_1_url, product_2_url, product_3_url) is True


@pytest.mark.django_db
def test_non_active_product_not_there_active_there(client):
    category = Category.objects.create(name="Obuwie")
    non_active_product = Product.objects.create(
        is_active=False,
        category=category,
        name="Trampki",
        price=Decimal(20),
        short_description="Tanie dobre buty",
        full_description="Tanie dobre buty. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    active_product = Product.objects.create(
        is_active=True,
        category=category,
        name="Sandały",
        price=Decimal(100),
        short_description="Tanie dobre sandały",
        full_description="Tanie dobre sandały. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    non_active_product_url = CURRENT_DOMAIN + non_active_product.get_absolute_url()
    active_product_url = CURRENT_DOMAIN + active_product.get_absolute_url()
    url = reverse("django.contrib.sitemaps.views.sitemap")
    response = client.get(url)
    assert response.status_code == 200
    xml = response.content
    root = ET.fromstring(xml.decode())
    assert (
        xml_contains_texts(root, active_product_url) and
        not xml_contains_texts(root, non_active_product_url)
    )


@pytest.mark.django_db
def test_three_non_active_products_not_there(client):
    category = Category.objects.create(name="Obuwie")

    non_active_product_1 = Product.objects.create(
        is_active=False,
        category=category,
        name="Trampki",
        price=Decimal(20),
        short_description="Tanie dobre buty",
        full_description="Tanie dobre buty. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    non_active_product_2 = Product.objects.create(
        is_active=False,
        category=category,
        name="Sandały",
        price=Decimal(100),
        short_description="Tanie dobre sandały",
        full_description="Tanie dobre sandały. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    non_active_product_3 = Product.objects.create(
        is_active=False,
        category=category,
        name="Adidasy",
        price=Decimal(300),
        short_description="Tanie dobre adidast",
        full_description="Tanie dobre adidast. Bardzo tanie. Są czarne. Wytrzymałe"
    )
    url_product_1 = CURRENT_DOMAIN + non_active_product_1.get_absolute_url()
    url_product_2 = CURRENT_DOMAIN + non_active_product_2.get_absolute_url()
    url_product_3 = CURRENT_DOMAIN + non_active_product_3.get_absolute_url()
    url = reverse("django.contrib.sitemaps.views.sitemap")
    response = client.get(url)
    assert response.status_code == 200
    xml = response.content
    root = ET.fromstring(xml.decode())
    assert (
        not xml_contains_texts(root, url_product_1) and
        not xml_contains_texts(root, url_product_2) and
        not xml_contains_texts(root, url_product_3)
    )