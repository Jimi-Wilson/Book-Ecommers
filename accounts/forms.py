from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required. Add a valid email Address')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
