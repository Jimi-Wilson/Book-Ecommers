from LibraryApp.forms import ShippingAddressForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator

from .forms import UserUpdateForm, RegistrationForm

from .models import User

from django.views import View
from django.views.generic import *
from django.urls import reverse_lazy


class Register(View):
    def get(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
        return render(request, 'register.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        shipping_form = ShippingAddressForm(
            instance=request.user.shipping_address)
        user_form = UserUpdateForm(instance=request.user)

        context = {'shipping_form': shipping_form, 'user_form': user_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        shipping_form = ShippingAddressForm(
            request.POST, instance=request.user.shipping_address)
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if shipping_form.is_valid() and user_form.is_valid():
            shipping_address = shipping_form.save()
            request.user.shipping_address = shipping_address
            request.user.save()

            user_form.save()
            return redirect('profile')
        else:
            context = {'shipping_form': shipping_form, 'user_form': user_form}
            return render(request, self.template_name, context)
