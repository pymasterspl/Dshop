from django.views.generic import ListView, DetailView
from .models import Product


# Create your views here.
class ProductListView(ListView):

    model = Product
    template_name = 'products_catalogue/products_list.html'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductDetailView(DetailView):

    model = Product
    template_name = 'products_catalogue/product_detail.html'
    context_object_name = 'product'
    queryset = Product.objects.filter(is_active=True)
