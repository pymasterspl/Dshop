import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from lxml import etree
from dj_shop_cart.cart import Cart

from .models import Product, CeneoCategory, Category


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
                id=product.id) | Product.objects.filter(id=product.parent_product.id)
        else:
            product_variants = Product.objects.filter(parent_product=product).exclude(id=product.id)
        context['attributes'] = attributes
        context['product_variants'] = product_variants
        return context


class AddToCartView(CreateView):
    model = Cart

    def get(self, request, **kwargs):
        quantity = 1
        cart = self.model.new(request)
        product_id = self.kwargs.get('id')
        product = get_object_or_404(Product, id=product_id)

        cart.add(product,  quantity=quantity)

        return redirect('cart_detail_view')


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


class CeneoCategoriesView(View):

    @staticmethod
    def fetch_ceneo_data():
        url = 'https://developers.ceneo.pl/api/v3/kategorie'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise CeneoAPIException(f"Failed to fetch data from Ceneo API: {e}")

    # TODO: to add parent category to the model and add functionality to write it to database
    def parse_categories(self, category_elem):
        categories = []
        for elem in category_elem:
            category = {
                'Id': int(elem.findtext('Id')),
                'name': elem.findtext('Name'),
            }
            subcategories_elem = elem.find('Subcategories')
            if subcategories_elem is not None:
                categories.extend(self.parse_categories(subcategories_elem))
            categories.append(category)
        return categories

    @staticmethod
    def import_ceneo_categories(categories):
        bulk_list = [CeneoCategory(id=category['Id'], name=category['name']) for category in categories]
        CeneoCategory.objects.bulk_create(bulk_list, ignore_conflicts=True, update_conflicts=False)

    def get(self, request, *args, **kwargs):
        xml_data = self.fetch_ceneo_data()
        root = etree.fromstring(xml_data)
        categories = self.parse_categories(root)
        for category in categories:
            category['Id'] = int(category['Id'])
        categories.sort(key=lambda x: x['Id'])
        self.import_ceneo_categories(categories)
        return HttpResponse('Ceneo categories data imported successfully.', 200)


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
        products_without_parent = Product.objects.filter(category=self.get_object(), parent_product=None)
        context['products'] = products_without_parent
        return context
    