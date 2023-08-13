# from django.test import TestCase
# from .models import Category
#
#
# class TestCategoriesModels(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(
#             name='Biuro i praca',
#             is_active=True,
#         )
#
#     def test_create_category(self):
#         self.assertIsInstance(self.category, Category)
#
#     def test_category_slug(self):
#         self.assertEqual(self.category.slug, 'biuro-i-praca')
