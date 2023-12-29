from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import serialize_cart
from dj_shop_cart.cart import get_cart_class


class CartAPIView(APIView):
    def post(self, request, id, quantity):
        cart = get_cart_class().new(request)
        product = get_object_or_404(Product, id=id)

        if not product.is_available:
            raise ValidationError("Produkt jest niedostępny.")
        if quantity <= 0:
            raise ValidationError("Nieprawidłowa ilość")
        cart.add(product,  quantity=quantity)
        return Response(serialize_cart(cart), status=status.HTTP_201_CREATED)


    def get(self, request):
        cart = get_cart_class().new(request)
        return Response(serialize_cart(cart), status=status.HTTP_200_OK)
    
    def delete(self, request, item_id, quantity=None):
        cart = get_cart_class().new(request)    
        if quantity is None:
            result = cart.remove(item_id=item_id)
            if not result:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif quantity <= 0:
            raise ValidationError("Nieprawidłowa ilość")
        else:
            result = cart.remove(item_id=item_id, quantity=quantity)
            if not result:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)