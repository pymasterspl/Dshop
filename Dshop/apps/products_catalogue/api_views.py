from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dj_shop_cart.cart import get_cart_class

from .models import Product
from .serializers import CartReadSerializer, ProductSerializer, CartWriteSerializer
from .filters import ProductFilter
from .api_permissions import IsStaffOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True, parent_product=None)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = (IsStaffOrReadOnly, )

class CartAPIView(APIView):
    def post(self, request):
        serializer = CartWriteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart = serializer.save()
            read_serializer = CartReadSerializer(cart)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        cart = get_cart_class().new(request)
        serializer = CartReadSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
