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