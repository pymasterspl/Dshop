from django.urls import path, include
from .api_views import OrderAPIView, ProductViewSet, CartAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products/', ProductViewSet, basename='products-api')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartAPIView.as_view(), name="api_cart"),
    path('order/', OrderAPIView.as_view(), name="api_order")
]
