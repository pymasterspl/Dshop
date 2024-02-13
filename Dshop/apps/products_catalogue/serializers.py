from rest_framework import serializers

from .models import Product, Order



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'short_description', 'full_description', 'parent_product']
        read_only_fields = ['id']



class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['user','delivery',
                  'created_at','cart_details',
                  'cart_total','delivery_name',
                  'delivery_price','total_sum']
       

    def create(self, validated_data):
        request = self.context.get('request')
        instance = Order.create_cart(request, **validated_data)
        return instance
   