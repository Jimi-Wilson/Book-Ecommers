from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import isStaff


from .forms import *
from Inventory.models import Book
from accounts.models import User


@login_required
@isStaff
def home(request):
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
@isStaff
def staffRegister(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)


@login_required
@isStaff
def addBook(request):
    if request.method == 'POST':
        form = addBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')

    form = addBookForm()

    context = {'form' : form}
    return render(request, 'addBook.html', context)
