from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customusers', verbose_name=_('User'))
    first_name = models.CharField(max_length=100, blank=True, verbose_name=_('First name'))
    last_name = models.CharField(max_length=100, blank=True, verbose_name=_('Last name'))
    address = models.CharField(max_length=150, blank=True, verbose_name=_('Address'))
    postal_code = models.CharField(max_length=7, blank=True, verbose_name='ZIP/Postal code')
    city = models.CharField(max_length=50, blank=True, verbose_name=_('City'))
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL, related_name='customusers')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of birth'))
    phone_number = models.CharField(max_length=15, blank=True, verbose_name=_('Phone number'))
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
