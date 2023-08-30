from django.urls import path
from .views import CeneoProductListView, CeneoCategoriesView


urlpatterns = [
    path('ceneo/', CeneoProductListView.as_view(), name='product-list'),
    path('ceneo_categories/', CeneoCategoriesView.as_view, name='ceneo-categories'),
]
