from dj_shop_cart.cart import CartItem
from django.db import models
from django.db.models import DecimalField
from django.utils.text import slugify
from tinymce import models as tinymce_models


class CatalogueItemModel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, editable=False, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # for creating urls use {% url "url-name" item.slug item.pk %}
        # path('<slug:slug>-<int:pk>/', NoteDetailView.as_view(), name='note_details'),
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class CeneoCategory(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'CeneoCategory'
        verbose_name_plural = 'CeneoCategories'

    def __str__(self):
        return self.name


class Category(CatalogueItemModel):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    ceneo_category = models.ForeignKey(CeneoCategory, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Product(CatalogueItemModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_price_last_30_days = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_description = tinymce_models.HTMLField()
    full_description = tinymce_models.HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    availability = models.PositiveSmallIntegerField(choices=[
        (1, 'Dostępny, sklep wyśle produkt w ciągu 24 godzin'),
        (3, 'Sklep wyśle produkt do 3 dni'),
        (7, 'Sklep wyśle produkt w ciągu tygodnia'),
        (14, 'Sklep wyśle produkt do 14 dni'),
        (90, 'Towar na zamówienie'),
        (99, 'Brak informacji o dostępności - status „sprawdź w sklepie”'),
        (110, 'Przedsprzedaż'),
    ], default=99)

    @property
    def featured_photos(self):
        return ProductImage.objects.filter(product=self, is_featured=True)

    def get_price(self, item: CartItem) -> DecimalField:

        return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/')
    is_featured = models.BooleanField(default=False)
