from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import is_staff

from .forms import *
from Inventory.models import Book
from accounts.models import User


@login_required
@is_staff
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

    return render(request, "inventory/home.html", context)


@login_required
@is_staff
def staff_register(request):
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
@is_staff
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')

    form = AddBookForm()

    context = {'form': form}
    return render(request, 'inventory/addBook.html', context)


@login_required
@is_staff
def view_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'inventory/viewBooks.html', context)


@login_required
@is_staff
def update_book(request, id):
    book = Book.objects.get(id=id)
    form = AddBookForm(instance=book)
    if request.method == 'POST':
        form = AddBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('viewBooks')

    context = {'form': form}
    return render(request, 'inventory/updateBook.html', context)

@login_required
@is_staff
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('viewBooks')