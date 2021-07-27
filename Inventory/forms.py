from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from Inventory.models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'staff')


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title',
                  'author',
                  'description',
                  'barcode',
                  'price',
                  'borrowed',
                  'coverImage')


class SearchBookForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder':'Title'}), label='')
    author = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder':'Author'}), label='')
    barcode = forms.CharField(max_length=13, required=False, widget=forms.TextInput(attrs={'placeholder':'Barcode'}), label='')
