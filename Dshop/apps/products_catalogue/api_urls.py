from django.urls import path, include
from .api_views import ProductViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products-api')
router.register(r'orders', OrderViewSet, basename='orders-api')

urlpatterns = [
    path('', include(router.urls)),
]
