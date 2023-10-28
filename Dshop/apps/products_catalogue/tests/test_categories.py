import pytest
from apps.products_catalogue.models import Category
from django.urls import reverse


NON_EXISTING_SLUG = "xzcvbnmzxc"


@pytest.mark.django_db
def test_get_categories_list(client):
    cat_1 = Category.objects.create(name="Koszule")
    cat_2 = Category.objects.create(name="Buty")
    cat_3 = Category.objects.create(name="Druty")
    url = reverse("category-list")
    response = client.get(url)
    categories = response.context["categories"]
    assert response.status_code == 200
    assert (
        cat_1 in categories and
        cat_2 in categories and
        cat_3 in categories
    )


@pytest.mark.django_db
def test_get_empty_categories_list(client):
    url = reverse("category-list")
    response = client.get(url)
    assert response.status_code == 200
    categories = response.context["categories"]
    assert len(categories) == 0


@pytest.mark.django_db
def test_get_non_active_categories_list(client):
    cat_1 = Category.objects.create(name="Koszule", is_active=False)
    cat_2 = Category.objects.create(name="Buty", is_active=False)
    cat_3 = Category.objects.create(name="Druty", is_active=False)
    url = reverse("category-list")
    response = client.get(url)
    assert response.status_code == 200
    categories = response.context["categories"]
    assert len(categories) == 0


@pytest.mark.django_db
def test_get_categories_detail_by_reversed_url(client):
    cat = Category.objects.create(name="Kategoria")
    url = reverse('category-detail', args=[cat.slug, cat.id])
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['category'], Category)


@pytest.mark.django_db
def test_get_categories_detail_by_absolute_url(client):
    cat = Category.objects.create(name="Kategoria")
    url = cat.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['category'], Category)


@pytest.mark.django_db
def test_get_invalid_slug_categories_detail(client):
    cat = Category.objects.create(name="Kategoria")
    url = reverse('category-detail', args=[NON_EXISTING_SLUG, cat.id])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_non_active_categories_detail(client):
    cat = Category.objects.create(name="Kategoria", is_active=False)
    url = reverse('category-detail', args=[cat.slug, cat.id])
    response = client.get(url)
    assert response.status_code == 404
