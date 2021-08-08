from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from Inventory.models import *


class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Type Your Email Address'}))
    firstName = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Type Your First Name'}),
        label="First Name:")
    lastName = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Type Your Last Name'}),
        label="Last Name:")

    class Meta:
        model = User
        fields = ('email', 'firstName', 'lastName', 'password1', 'password2',
                  'staff')


class AddBookForm(forms.ModelForm):
    tags = Tag.objects.all()
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Type The Title'}))

    author = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Type The Author'}))

    description = forms.CharField(
        max_length=400,
        widget=forms.Textarea(attrs={'placeholder': 'Type The Description'}))

    barcode = forms.CharField(
        max_length=13,
        min_length=13,
        widget=forms.TextInput(attrs={'placeholder': 'Type The Barcode'}))

    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'placeholder': 'Type The Price'}), )

    discounted_price = forms.DecimalField(
        required=False,
        help_text='This Fields Is Not Required',
        widget=forms.NumberInput(
            attrs={'placeholder': 'Type The Discount Price'}))

    coverImage = forms.ImageField(label='Book Cover :')
    tags = forms.ModelMultipleChoiceField(
        tags, help_text='Hold CTRL To Select Multiple', required=False)

    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'barcode', 'price',
                  'discounted_price', 'borrowed', 'coverImage', 'tags')


class SearchBookForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Type The Title'}))
    author = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Type The Author'}))
    barcode = forms.CharField(
        max_length=13,
        min_length=13,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Type The Barcode'}))
    tags = Tag.objects.all()
    tags = forms.ModelMultipleChoiceField(
        tags, help_text='Hold CTRL To Select Multiple', required=False)


class AddTagForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Type In The Tag Name'}))

    class Meta:
        model = Tag
        fields = ('name', )
