from django.db import transaction
from django.shortcuts import get_object_or_404
from dj_shop_cart.cart import get_cart_class
from rest_framework import serializers
from .models import Product, Order, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

        
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'short_description', 'full_description', 'parent_product', 'images']
        read_only_fields = ['id']


class CartItemSerializer(serializers.Serializer):
    product_pk = serializers.IntegerField(min_value=1, required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
    product_name = serializers.CharField(read_only=True, max_length=200)
    price = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    subtotal = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    item_id = serializers.IntegerField(read_only=True, min_value=1)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_name = Product.objects.get(pk=instance.product_pk).name
        representation['product_name'] = product_name
        return representation


class CartReadSerializer(serializers.Serializer):
    total = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    items = serializers.SerializerMethodField()
    count = serializers.IntegerField(read_only=True, min_value=1)

    def get_items(self, obj):
        return CartItemSerializer(list(obj), many=True).data


class CartWriteSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True, required=False)

    def create(self, validated_data):
        request = self.context['request']
        cart = get_cart_class().new(request)
        cart.empty()
        with transaction.atomic():
            for item in validated_data.get("items", []):
                product = get_object_or_404(Product, pk=item['product_pk'])
                cart.add(product, quantity=item['quantity'])
        return cart
    

    def validate_items(self, items):
        product_pks = set()
        for item in items:
            product_pk = item.get("product_pk")
            if product_pk in product_pks:
                raise serializers.ValidationError(
                    "product_pk must be unique within items."
                )
            product_pks.add(product_pk)
        return items
    

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['delivery',
                  'created_at','cart_details',
                  'cart_total','delivery_name',
                  'delivery_price','total_sum']
       

    def create(self, validated_data):
        request = self.context.get('request')
        instance = Order.create_cart(request, **validated_data)
        return instance
    

