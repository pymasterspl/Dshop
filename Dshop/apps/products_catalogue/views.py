from lxml import etree

from django.http import HttpResponse
from django.views.generic import ListView

from .models import Product


class ProductListView(ListView):
    model = Product

    def generate_xml_file_for_ceneo(self, products):
        root = etree.Element('offers', xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance", version="1")

        for product in products:
            o_element = etree.SubElement(root, 'o', id=str(product.pk), url=str(), price=str(product.price),
                                         avail=str())  # TODO: url and available items

            cat_element = etree.SubElement(o_element, 'cat')
            cat_element.text = etree.CDATA(product.category.name)

            name_element = etree.SubElement(o_element, 'name')
            name_element.text = etree.CDATA(product.name)

            imgs_element = etree.SubElement(o_element, 'imgs')
            main_element = etree.SubElement(imgs_element, 'main', url=str(product.images))  # TODO: get correct url

            desc_element = etree.SubElement(o_element, 'desc')
            desc_element.text = etree.CDATA(product.full_description)

            attrs_element = etree.SubElement(o_element, 'attrs')  # TODO: add <a>
            attrs_element.text = etree.CDATA('')

        xml_string = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        response = HttpResponse(xml_string, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="ceneo.xml"'
        return response

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        xml_response = self.generate_xml_file_for_ceneo(products)
        return xml_response
