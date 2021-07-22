from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import *
from .models import Book
from accounts.models import User


@login_required
def home(request):

    user = request.user
    if not user.is_staff:
        return render(request, 'invalidCredentials.html')
    context = {}
    books = Book.objects.all()
    customers = User.objects.all()
    customers = customers.filter(admin=False, staff=False)

    totalBooks = books.count()
    context['totalBooks'] = totalBooks
    borrowedBooks = books.filter(borrowed=True).count()
    context['borrowedBooks'] = borrowedBooks
    totalCustomers = customers.count()
    context['totalCustomers'] = totalCustomers


    return render(request, "inventoryHome.html", context)

@login_required
def staffRegister(request):
    user = request.user
    if not user.is_staff:
        return render(request, 'invalidCredentials.html')
    context = {}
    if request.POST:
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
    else:
         form = RegistrationForm()
         context['registration_form'] = form
    return render(request, 'register.html', context)


def addBook(request):
    user = request.user
    if not user.is_staff:
        return render(request, 'invalidCredentials.html')
    context = {}
    if request.POST:
        form = add_Book(request.POST, request.FILES)
        if form.is_valid():
            pass
        else:
            context['form'] = form
    form = add_Book()
    context['form'] = form
    return render(request, 'addBook.html', context)