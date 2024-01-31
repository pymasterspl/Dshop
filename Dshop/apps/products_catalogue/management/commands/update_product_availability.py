from django.core.management.base import BaseCommand

from Dshop.apps.products_catalogue.models import Product


class Command(BaseCommand):
    help = 'Update availability to 99 (No information about availability - status "check in store") for all products.'

    def handle(self, *args, **kwargs):
        Product.objects.update(availability=99)

        self.stdout.write(self.style.SUCCESS('Updated availability to 99 for all products.'))
