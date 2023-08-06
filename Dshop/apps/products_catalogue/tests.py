from django.test import TestCase
from .models import Category, SubCategory


class TestCategoriesModels(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Category',
            slug='category',
            is_active=True,
            sort=1
        )
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name='Subcategory',
            slug='subcategory',
            is_active=True,
            sort=1
        )

    def test_create_category(self):
        self.assertIsInstance(self.category, Category)

    def test_create_subcategory(self):
        self.assertIsInstance(self.subcategory, SubCategory)
