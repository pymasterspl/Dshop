from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from .filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True, parent_product=None)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class OrderViewSet(viewsets.ModelViewSet):
   
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
       

    