from django.urls import path
from .views import ProductListView, GetCeneoCategories


urlpatterns = [
    path('ceneo/', ProductListView.as_view(), name='product-list'),
    path('get_ceneo_categories/', GetCeneoCategories, name='get-ceneo-categories'),
]
