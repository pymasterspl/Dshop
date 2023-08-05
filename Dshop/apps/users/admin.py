from django.contrib import admin
from .models import CustomUser, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['code']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email')
    search_fields = ['user__username', 'user__email']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Login'
    get_username.admin_order_field = 'user__login'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

