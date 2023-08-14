import pytest
from django.db import IntegrityError
from .models import Category


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
def test_create_duplicate_slug():
    Category.objects.create(name='Main Category', is_active=True)
    with pytest.raises(IntegrityError):
        Category.objects.create(name='Main Category', is_active=True)