import logging

import requests
from django.core.management.base import BaseCommand
from lxml import etree

from apps.products_catalogue.models import CeneoCategory

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = 'Update Ceneo categories in the database.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching Ceneo data...')
        xml_data = self.fetch_ceneo_data()
        root = etree.fromstring(xml_data)
        categories = self.parse_categories(root)
        for category in categories:
            category['id'] = int(category['id'])
        categories.sort(key=lambda x: x['id'])
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
            logging.error(f"Failed to fetch data from Ceneo API: {e}")
            raise

    def parse_categories(self, category_elem):
        categories = []
        for elem in category_elem:
            category = {
                'id': int(elem.findtext('Id')),
                'name': elem.findtext('Name'),
            }
            subcategories_elem = elem.find('Subcategories')
            if subcategories_elem is not None:
                categories.extend(self.parse_categories(subcategories_elem))
            categories.append(category)
        return categories

    @staticmethod
    def import_ceneo_categories(categories):
        existing_categories = set(CeneoCategory.objects.values_list('id', flat=True))
        new_categories = []

        for category in categories:
            if category['id'] in existing_categories:
                logging.info(f"Category {category['id']} ({category['name']}) already exists.")
            else:
                new_categories.append(CeneoCategory(id=category['id'], name=category['name']))

        if new_categories:
            CeneoCategory.objects.bulk_create(new_categories, ignore_conflicts=True, update_conflicts=False)
            logging.info(f"Imported {len(new_categories)} new Ceneo categories.")
        else:
            logging.info("No new categories to import.")
