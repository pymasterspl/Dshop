from dj_shop_cart.cart import CartItem
from django.db import models
from django.db.models import DecimalField
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.urls import reverse
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
    updated_at = models.DateTimeField(auto_now=True)

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


    def get_absolute_url(self):
        return reverse("category-detail", args=[self.slug, self.id])


class Product(CatalogueItemModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
    parent_product = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse("product-detail", args=[self.slug, self.id])

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.current_price = self.price

    def save(self, *args, **kwargs):
        created = not self.pk
        super(Product, self).save(*args, **kwargs)
        last_price_change = PriceChangeHistory.objects.filter(product=self).order_by('created_at').last()
        if self.current_price != self.price or created:
            price_change = PriceChangeHistory.objects.create(product=self, price=self.price)
            if last_price_change:
                last_price_change.disabled_at = price_change.created_at
                last_price_change.save()

    @property
    def featured_photos(self):
        return ProductImage.objects.filter(product=self, is_featured=True)

    @property
    def lowest_price_in_30_days(self):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        price_changes = self.price_change_history.filter(disabled_at__gte=thirty_days_ago).order_by('price')
        if price_changes:
            return Decimal(min(price_changes[0].price, self.price))
        else:
            return Decimal(self.price)

    def get_price(self, item: CartItem) -> DecimalField:

        return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/')
    is_featured = models.BooleanField(default=False)

class PriceChangeHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_change_history')
    created_at = models.DateTimeField(auto_now_add=True)
    disabled_at = models.DateTimeField(null=True, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
