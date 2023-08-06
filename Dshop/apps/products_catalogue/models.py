from django.db import models


class CategoryBaseModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    sort = models.IntegerField(default=99)

    class Meta:
        ordering = ('sort',)
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryBaseModel):

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class SubCategory(CategoryBaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'


