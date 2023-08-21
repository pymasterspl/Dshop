from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    readonly_fields = ('slug',)


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'price_last_30_days')
    search_fields = ('name',)
    inlines = [ProductImageInLine]


admin.site.register(Product, ProductAdmin)
