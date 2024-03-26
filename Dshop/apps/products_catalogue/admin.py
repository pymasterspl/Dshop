from django.contrib import admin
from .models import (Category, Product, ProductImage, 
                     CeneoCategory, ProductAttribute,
                     DeliveryMethod, Order)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    readonly_fields = ('slug',)


class ProductAttributeInLine(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    inlines = [ProductImageInLine, ProductAttributeInLine]
    readonly_fields = ('id', 'slug',)

@admin.register(CeneoCategory)
class CeneoCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ('name',)
    ordering = ('name',)
    


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('id','name','price')
    search_fields = ('name','price')
    ordering = ('name','price')
    

@admin.register(Order)
class OrderMethodAdmin(admin.ModelAdmin):
    list_display = ('user','delivery',
                  'created_at','cart_details',
                  'cart_total','delivery_name',
                  'delivery_price','total_sum')