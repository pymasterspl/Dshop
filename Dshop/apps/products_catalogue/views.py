from django.views import View
from lxml import etree
import xml.etree.ElementTree as ET
import requests
from django.http import HttpResponse

from .models import Product, CeneoCategory


class ProductListView(View):
    model = Product

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        return queryset

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
            main_element = etree.SubElement(imgs_element, 'main')

            main_element.set('url', str(product.images)) # TODO: get correct url

            desc_element = etree.SubElement(o_element, 'desc')
            desc_element.text = etree.CDATA(product.full_description)

            attrs_element = etree.SubElement(o_element, 'attrs')  # TODO: add <a>
            attrs_element.text = etree.CDATA('')

        xml_string = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        response = HttpResponse(xml_string, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="ceneo.xml"'
        return response

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()

        xml_response = self.generate_xml_file_for_ceneo(products)
        return xml_response

def getCeneoCategories(request):
    
    url = 'https://developers.ceneo.pl/api/v3/kategorie'
    response = requests.get(url)
    xml_data = response.content
    
    root  = ET.fromstring(xml_data)
    

    def parse_category(category_elem):
        category = {
            'Id': category_elem.find('Id').text,
            'name': category_elem.find('Name').text,         
        }
        return category

    def parse_categories(category_elem):
        categories = []
        for elem in category_elem:
            category = parse_category(elem)
            subcategories_elem = elem.find('Subcategories')
            if subcategories_elem is not None:
                categories.extend(parse_categories(subcategories_elem))
            categories.append(category)
        return categories
    

    categories = parse_categories(root)

    for x in categories:
        x['Id']=int(x['Id'])

    categories.sort(key = lambda x: x['Id'])
    bulk_list =[CeneoCategory(id=category['Id'], name=category['name']) for category in categories ]
    bulk_msg =CeneoCategory.objects.bulk_create(bulk_list, ignore_conflicts=True, update_conflicts=False)
    print(bulk_msg)
    

    return HttpResponse('OK')

