from django.urls import path
from .views import ProductListView, getCeneoCategories


urlpatterns = [
    path('ceneo/', ProductListView.as_view(), name='product-list'),
    path('get_ceneo_categories/', getCeneoCategories, name='get-ceneo-categories'),
]
