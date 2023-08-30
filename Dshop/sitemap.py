from django.contrib.sitemaps import Sitemap
from apps.products_catalogue.models import Product, Category

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority =0.9
    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at

# class CategorySitemap(Sitemap):
#     changefreq = 'weekly'
#     priority =0.9
#     def items(self):
#         return Category.objects.all()
    
#     def lastmod(self, obj):
#         return obj.updated_at