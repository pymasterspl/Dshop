from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductListView, ProductsDetailView

urlpatterns = [

    # R
    path('products_list/', ProductListView.as_view(), name='products-list'),
    path('pd/<slug:slug>-<int:pk>', ProductsDetailView.as_view(), name="products-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)