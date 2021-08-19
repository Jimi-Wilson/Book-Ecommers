from django import forms
from Inventory.models import *


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('complete', )