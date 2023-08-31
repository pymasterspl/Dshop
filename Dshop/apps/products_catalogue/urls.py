from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductListView, ProductDetailView

urlpatterns = [

    # R
    path('products_list/', ProductListView.as_view(), name='products-list'),
    path("products/<slug>", ProductDetailView.as_view(), name='product-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)