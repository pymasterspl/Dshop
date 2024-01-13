from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True, parent_product=None)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
