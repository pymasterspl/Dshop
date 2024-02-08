from django.urls import path, include
from .api_views import ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ProductViewSet, basename='products-api')

urlpatterns = [
    path('', include(router.urls)),
]
