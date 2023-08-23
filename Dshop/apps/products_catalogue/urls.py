from django.urls import path
from .views import ProductListView


urlpatterns = [
    path('ceneo/', ProductListView.as_view(), name='product-list'),
]
