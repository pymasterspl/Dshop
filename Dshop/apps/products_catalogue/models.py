from dj_shop_cart.cart import CartItem
from django.db import models
from django.db.models import DecimalField
from django.utils.text import slugify
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


# TODO : CeneoCategory class must have self FK as it is in Category class
class CeneoCategory(models.Model):
    name = models.CharField(max_length=200)

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
    lowest_price_last_30_days = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_description = tinymce_models.HTMLField()
    full_description = tinymce_models.HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("product-detail", args=[self.slug, self.id])

    def __str__(self):
        return self.name

    @property
    def featured_photos(self):
        return ProductImage.objects.filter(product=self, is_featured=True)

    def get_price(self, item: CartItem) -> DecimalField:

        return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/')
    is_featured = models.BooleanField(default=False)
