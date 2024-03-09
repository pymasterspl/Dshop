from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from dj_shop_cart.cart import get_cart_class
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import CartReadSerializer, ProductSerializer, CartWriteSerializer
from .filters import ProductFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True, parent_product=None)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = (AllowAny, )

class CartAPIView(APIView):
    permission_classes = (AllowAny ,)
    serializer_class = CartReadSerializer
    
    def post(self, request):
        write_serializer = CartWriteSerializer(data=request.data, context={'request': request})
        if write_serializer.is_valid():
            cart = write_serializer.save()
            return Response(self.serializer_class(cart).data, status=status.HTTP_201_CREATED)
        else:
            return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        cart = get_cart_class().new(request)
        serializer = self.serializer_class(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
