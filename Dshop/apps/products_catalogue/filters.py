from django.forms import TextInput
from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains',
                              widget=TextInput(attrs={'placeholder': 'Szukaj po nazwie'}))
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt',
                                     widget=TextInput(attrs={'placeholder': 'max'}))
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt',
                                     widget=TextInput(attrs={'placeholder': 'min'}))
    category_name = filters.ChoiceFilter(field_name='category__name',
                                         choices=Category.objects.all().values_list('name', 'name').distinct(),
                                         label='Category', empty_label='Wybierz Kategorie')
    order_by = filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('name', 'name'),
        ),
        field_labels={
            'price': 'Cena rosnąco',
            '-price': 'Cena malejąco',
            '-name': 'Produkt A-Z',
            'name': 'Produkt Z-A',
        },
        label='Sortuj',
        empty_label='Domyślnie'
    )

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)
        self.filters['name'].label = 'Nazwa produktu'
        self.filters['price__lt'].label = 'Cena do'
        self.filters['price__gt'].label = 'Cena od'
        self.filters['order_by'].label = 'Sortowanie'
        self.filters['category_name'].label = 'Kategoria'

    class Meta:
        model = Product
        fields = ['name', 'price', 'category_name']
