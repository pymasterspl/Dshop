from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'short_description', 'full_description', 'parent_product']
        read_only_fields = ['id']
