from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CeneoCategoriesView, CeneoProductListView, ProductListView

urlpatterns = [
    path('products_list/', ProductListView.as_view(), name='products-list'),
    path('ceneo/', CeneoProductListView.as_view(), name='product-list'),
    path('ceneo_categories/', CeneoCategoriesView.as_view(), name='ceneo-categories'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
