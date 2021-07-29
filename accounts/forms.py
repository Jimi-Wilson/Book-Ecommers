from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Type Your Email Address'}))
    firstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type Your First Name'}), label="First Name:")
    lastName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type Your Last Name'}), label="Last Name:")

    class Meta:
        model = User
        fields = ('firstName','lastName','email', 'password1', 'password2')
