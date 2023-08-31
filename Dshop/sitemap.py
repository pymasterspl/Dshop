from django.contrib.sitemaps import Sitemap
from apps.products_catalogue.models import Product, Category
from django.urls import reverse


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority =0.9
    def items(self):
        return Product.objects.order_by("-id")

    def lastmod(self, obj):
        return obj.updated_at

# class CategorySitemap(Sitemap):
#     changefreq = 'weekly'
#     priority =0.9
#     def items(self):
#         return Category.objects.all()

#     def lastmod(self, obj):
#         return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ["products-list"]

    def location(self, item):
        return reverse(item)