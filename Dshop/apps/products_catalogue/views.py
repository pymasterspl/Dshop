#from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView
from .models import Product

class IndexView(ListView):
    template_name = "index.html"
    model = Product