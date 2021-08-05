from Inventory.models import OrderItem
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
