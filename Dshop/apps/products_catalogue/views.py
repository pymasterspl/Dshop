from django.views.generic import View, TemplateView
from django.views.generic import ListView
from .models import Product
import datetime


# Create your views here.
class ProductListView(ListView):

    model = Product
    template_name = 'products_catalogue/products_list.html'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)



