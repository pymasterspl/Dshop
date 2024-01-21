from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import CartSerializer
from dj_shop_cart.cart import get_cart_class


class CartAPIView(APIView):
    
    @transaction.atomic
    def post(self, request):
        # TU?
        serializer = CartSerializer(data=request.data)
        serializer.is_valid()
        print(f"{serializer.validated_data=}")
        cart = get_cart_class().new(request)
        cart.empty()
        for el in request.data.get("items"):
            print(f"{el=}")
            product = get_object_or_404(Product, pk=el.get("product_pk"))
            cart.add(product, quantity=el.get("quantity"))
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    def get(self, request):
        cart = get_cart_class().new(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)#