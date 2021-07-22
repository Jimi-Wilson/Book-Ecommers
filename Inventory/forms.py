from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from .models import *


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required. Add a valid email Address')
    staff = forms.BooleanField()

    class Meta:
        model = User
        fields = ('email', 'password1','password2','staff')


class add_Book(forms.Form):
    title = forms.CharField(max_length=100)
    author = forms.CharField(max_length=100)
    description = forms.CharField(max_length=400)
    barcode = forms.CharField(max_length=13)
    price = forms.FloatField()
    coverImage = forms.ImageField()
    borrowed = False
