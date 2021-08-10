from django.db import models
from django.db.models import fields
from django.db.models.fields import files
from Inventory.models import OrderItem, ShippingAddress, BillingAddress
from django import forms


class SearchForm(forms.Form):
    search_field = forms.CharField(
        max_length=200,
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'search-box',
            'placeholder': 'Search...'
        }))


class CartQuantityForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ('quantity', )


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = '__all__'