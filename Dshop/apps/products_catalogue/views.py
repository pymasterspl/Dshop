from dj_shop_cart.cart import get_cart_class, Cart
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from lxml import etree

from .models import Product, Category


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        attributes = product.get_attributes()
        if product.parent_product:
            product_variants = Product.objects.filter(parent_product=product.parent_product).exclude(
                id=product.id) | Product.objects.filter(id=product.parent_product.id, is_active=True)
        else:
            product_variants = Product.objects.filter(parent_product=product, is_active=True).exclude(id=product.id)
        context['attributes'] = attributes
        context['product_variants'] = product_variants
        return context


class AddToCartView(View):
    model = Cart

    def post(self, request, **kwargs):
        cart = self.model.new(request)
        product_id = self.kwargs.get('id')
        quantity = self.kwargs.get('quantity')
        product = get_object_or_404(Product, id=product_id)

        if not product.is_available:
            raise ValidationError("Produkt jest niedostępny.")

        cart.add(product, quantity=quantity)

        return redirect('cart_detail')


class DeleteOneCartItemView(DeleteView):
    model = Cart

    def post(self, request, **kwargs):
        cart = self.model.new(request)
        item_id = self.kwargs.get('item_id')

        cart.remove(item_id=item_id, quantity=1)

        return redirect('cart_detail')


class DeleteCartItemView(DeleteView):
    model = Cart

    def post(self, request, **kwargs):
        cart = get_cart_class().new(request)
        item_id = self.kwargs.get('id')
        cart.remove(item_id=item_id)

        return redirect('cart_detail')


class CartDetailView(View):
    model = Cart

    def get(self, request):
        cart = self.model.new(request)

        return render(
            request,
            'products_catalogue/cart_detail.html',
            {'cart': cart}
        )


class CeneoProductListView(View):
    model = Product

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        return queryset

    @staticmethod
    def generate_xml_file_for_ceneo(products):
        root = etree.Element('offers', xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance", version="1")

        for product in products:
            o_element = etree.SubElement(root, 'o', id=str(product.pk), url=str(), price=str(product.price),
                                         avail=str(product.availability),  # TODO: add url
                                         weight=str(),
                                         stock=str(),
                                         basket=str())

            cat_element = etree.SubElement(o_element, 'cat')
            cat_element.text = etree.CDATA(product.category.name)

            name_element = etree.SubElement(o_element, 'name')
            name_element.text = etree.CDATA(product.name)

            if product.featured_photos.exists():
                featured_image_url = product.featured_photos.first().image.url
            else:
                featured_image_url = ''
            imgs_element = etree.SubElement(o_element, 'imgs')
            main_element = etree.SubElement(imgs_element, 'main')
            main_element.set('url', featured_image_url)

            additional_images = product.images.all()
            for i, additional_image in enumerate(additional_images, start=1):
                additional_img_element = etree.SubElement(imgs_element, 'i', id=str(i))
                additional_img_element.set('url', additional_image.image.url)

                if i >= 20:
                    break

            desc_element = etree.SubElement(o_element, 'desc')
            desc_element.text = etree.CDATA(product.full_description)

            attrs_element = etree.SubElement(o_element, 'attrs')  # TODO: add <a>
            attrs_element.text = etree.CDATA('')

        xml_string = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return xml_string

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()

        xml_string = self.generate_xml_file_for_ceneo(products)

        response = HttpResponse(xml_string, content_type='application/xml')
        return response


class CeneoAPIException(Exception):
    pass


class CategoryListView(ListView):
    context_object_name = 'categories'
    template_name = 'products_catalogue/categories_list.html'
    queryset = Category.objects.filter(is_active=True)


class CategoryDetailView(DetailView):
    template_name = 'products_catalogue/category_detail.html'
    context_object_name = 'category'
    queryset = Category.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_without_parent = Product.objects.filter(category=self.get_object(), parent_product=None,
                                                         is_active=True)
        context['products'] = products_without_parent
        return context
