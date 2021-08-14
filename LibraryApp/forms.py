from Inventory.models import OrderItem, Tag
from accounts.models import ShippingAddressModel
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
        model = ShippingAddressModel
        fields = [
            'first_line_of_address', 'seccond_line_of_address', 'postcode',
            'city'
        ]


class FilterForm(forms.Form):
    tags = Tag.objects.all()
    tags = forms.ModelMultipleChoiceField(
        tags, help_text='Hold CTRL To Select Multiple', required=False)
