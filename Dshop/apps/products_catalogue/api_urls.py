from django.urls import path, include
from .api_views import ProductViewSet, CartAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ProductViewSet, basename='products-api')

urlpatterns = [
    path('', include(router.urls)),
    path('cart', CartAPIView.as_view(), name="api_cart")
]
