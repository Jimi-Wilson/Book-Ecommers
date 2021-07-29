from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import is_staff
from django.shortcuts import get_object_or_404, render, redirect

from django.views import View
from django.views.generic import *
from django.urls import reverse_lazy

from .forms import *
from Inventory.models import Book
from accounts.models import User

decorators = [login_required, is_staff]


@method_decorator(decorators, name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        total_books = Book.objects.all().count()
        total_customers = User.objects.all().filter(admin=False,
                                                    staff=False).count()

        context['totalBooks'] = total_books
        context['totalCustomers'] = total_customers
        return render(request, 'inventory/home.html', context)


@method_decorator(decorators, name='dispatch')
class StaffRegister(CreateView):
    form_class = StaffRegistrationForm
    success_url = reverse_lazy('sHome')
    template_name = 'inventory/staffRegister.html'


@method_decorator(decorators, name='dispatch')
class AddBook(CreateView):
    form_class = AddBookForm
    success_url = reverse_lazy('viewBooks')
    template_name = 'inventory/addBook.html'


@method_decorator(decorators, name='dispatch')
class UpdateBook(UpdateView):
    form_class = AddBookForm
    success_url = reverse_lazy('viewBooks')
    queryset = Book.objects.all()
    template_name = 'inventory/updateBook.html'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Book, id=id)


@method_decorator(decorators, name='dispatch')
class DeleteBook(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        book = Book.objects.get(id=id)
        book.delete()
        return redirect('viewBooks')


@method_decorator(decorators, name='dispatch')
class ViewBooks(View):
    def get(self, request, *args, **kwargs):
        context = {}
        form = SearchBookForm()
        books = Book.objects.all()
        context['books'] = books
        context['form'] = form
        return render(request, 'inventory/viewBooks.html', context)

    def post(self, request, *args, **kwargs):
        filters = {}
        context = {}
        books = Book.objects.all()
        form = SearchBookForm(request.POST)
        if form.is_valid():
            title = form['title'].value().strip()
            if title:
                filters['title'] = title

            author = form['author'].value().strip()
            if author:
                filters['author'] = author

            barcode = form['barcode'].value().strip()
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


@method_decorator(decorators, name='dispatch')
class ViewTags(TemplateView):
    template_name = 'inventory/viewTags.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags'] = tags
        return context


@method_decorator(decorators, name='dispatch')
class AddTag(CreateView):
    form_class = AddTagForm
    success_url = reverse_lazy('viewTags')
    template_name = 'inventory/addTagForm.html'


@method_decorator(decorators, name='dispatch')
class UpdateTag(UpdateView):
    form_class = AddTagForm
    success_url = reverse_lazy('viewTags')
    template_name = 'inventory/updateBook.html'
    queryset = Tag.objects.all()

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Tag, id=id)


@method_decorator(decorators, name='dispatch')
class DeleteTag(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        tag = Tag.objects.get(id=id)
        tag.delete()
        return redirect('viewTags')