from django.shortcuts import render
from django.views import View
from .models import Product

# Create your views here.
class ProductListView(View):
    template_name = 'products_catalogue/products_list.html'
    model = Product
    def get(self, request):
        all_products = Product.objects.all()

        return render(request, self.template_name, {'all_products': all_products, })



