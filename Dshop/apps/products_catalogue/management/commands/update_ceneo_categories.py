import requests
from django.core.management.base import BaseCommand
from lxml import etree

from apps.products_catalogue.models import CeneoCategory
from apps.products_catalogue.views import CeneoAPIException


class Command(BaseCommand):
    help = 'Update Ceneo categories in the database.'

    def handle(self, *args, **kwargs):
        xml_data = self.fetch_ceneo_data()
        root = etree.fromstring(xml_data)
        categories = self.parse_categories(root)
        for category in categories:
            category['Id'] = int(category['Id'])
        categories.sort(key=lambda x: x['Id'])
        self.import_ceneo_categories(categories)
        self.stdout.write(self.style.SUCCESS('Ceneo categories data imported successfully.'))

    @staticmethod
    def fetch_ceneo_data():
        url = 'https://developers.ceneo.pl/api/v3/kategorie'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise CeneoAPIException(f"Failed to fetch data from Ceneo API: {e}")

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
