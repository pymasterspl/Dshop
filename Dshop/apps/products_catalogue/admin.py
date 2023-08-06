from django.contrib import admin
from .models import Category, SubCategory


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    prepopulated_fields = {'slug': ('name',)}

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'sort')
    list_editable = ('is_active', 'sort')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]
