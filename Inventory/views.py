from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import is_staff

from .forms import *
from Inventory.models import Book
from accounts.models import User


@login_required
@is_staff
def home(request, *args, **kwargs):
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
def staff_register(request, *args, **kwargs):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sHome')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'inventory\staffRegister.html', context)


@login_required
@is_staff
def add_book(request, *args, **kwargs):
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('sHome')

    form = AddBookForm()

    context = {'form': form}
    return render(request, 'inventory/addBook.html', context)


@login_required
@is_staff
def update_book(request, id, *args, **kwargs):
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
def delete_book(request, id, *args, **kwargs):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('viewBooks')


@login_required
@is_staff
def view_books(request, *args, **kwargs):
    filters = {}
    context = {}
    books = Book.objects.all()
    form = SearchBookForm()

    if request.method == 'POST':
        form = SearchBookForm(request.POST)
        if form.is_valid():
            title = form['title'].value()
            if title:
                filters['title'] = title

            author = form['author'].value()
            if author:
                filters['author'] = author

            barcode = form['barcode'].value()
            if barcode:
                filters['barcode'] = barcode

            tags = form['tags'].value()
            if tags:
                selected_books = books.filter(tags__in=tags)
                selected_books = selected_books.filter(**filters)
                context['books'] = selected_books
                context['form'] = form
                return render(request, 'inventory/viewBooks.html', context)

            selected_books = books.filter(**filters)
            if not selected_books:
                context['error'] = 'No Books Found'

            context['books'] = selected_books
            context['form'] = form
            return render(request, 'inventory/viewBooks.html', context)

    context['books'] = books
    context['form'] = form
    return render(request, 'inventory/viewBooks.html', context)


@login_required
@is_staff
def add_tag(request, *args, **kwargs):
    context = {}
    form = AddTagForm()
    if request.method == 'POST':
        form = AddTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sHome')
    context['form'] = form
    return render(request, 'inventory/addTagForm.html', context)


def view_tags(request, *args, **kwargs):
    context = {}
    tags = Tag.objects.all()
    context['tags'] = tags
    return render(request, 'inventory/viewTags.html', context)


@login_required
@is_staff
def update_tag(request, id, *args, **kwargs):
    tag = Tag.objects.get(id=id)
    form = AddTagForm(instance=tag)
    if request.method == 'POST':
        form = AddTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('viewBooks')

    context = {'form': form}
    return render(request, 'inventory/updateBook.html', context)


@login_required
@is_staff
def delete_tag(request, id, *args, **kwargs):
    tag = Tag.objects.get(id=id)
    tag.delete()
    return redirect('viewTags')
