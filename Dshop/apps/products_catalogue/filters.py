from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    is_active = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Product
        fields = ['name', 'is_active']
