# forms.py

from django import forms


class ShippingForm(forms.Form):
    selected_method = forms.ChoiceField(choices=[('courier', 'Kurier'), ('parcel_locker', 'Paczkomat')])
    selected_paczkomat = forms.CharField(required=False, max_length=255, label='Paczkomat ID',
                                         widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(max_length=255, label='Imię i nazwisko')
    street = forms.CharField(max_length=255, label='Ulica i numer domu')
    city = forms.CharField(max_length=255, label='Miejscowość')
    postal = forms.CharField(max_length=10, label='Kod pocztowy')
    info = forms.CharField(required=False, max_length=255, label='Dodatkowe informacje')
