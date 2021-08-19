from django.contrib.auth.decorators import login_required
from django.db.models.fields import files
from django.utils.decorators import method_decorator
from .decorators import is_staff
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import *
from django.urls import reverse_lazy

from .forms import *
from Inventory.models import Book
from accounts.models import User

from Library import settings
import stripe

decorators = [login_required, is_staff]


@method_decorator(decorators, name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        total_books = Book.objects.all().count()
        total_customers = User.objects.all().filter(admin=False,
                                                    staff=False).count()
        orders = Order.objects.all().filter(payment_complete=True,
                                            complete=False)
        context['orders'] = orders
        context['totalBooks'] = total_books
        context['totalCustomers'] = total_customers
        return render(request, 'inventory/home.html', context)


@method_decorator(decorators, name='dispatch')
class StaffRegisterView(CreateView):
    form_class = StaffRegistrationForm
    success_url = reverse_lazy('sHome')
    template_name = 'inventory/staffRegister.html'


@method_decorator(decorators, name='dispatch')
class AddBookView(View):
    form = AddBookForm
    success_url = reverse_lazy('viewBooks')
    template_name = 'inventory/addBook.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = AddBookForm(request.POST, request.FILES)
        context['form'] = form
        if form.is_valid():
            obj = form.save()
            stripe.api_key = settings.STRIPE_API_KEY
            product = stripe.Product.create(name=obj.title,
                                            description=obj.description)

            price = stripe.Price.create(
                product=product['id'],
                unit_amount=int(obj.price * 100),
                currency='gbp',
            )
            obj.payment_id = price['id']
            obj.product_id = product['id']

            obj.save()
            return redirect('viewBooks')
        return render(request, self.template_name, context)


@method_decorator(decorators, name='dispatch')
class UpdateBookView(UpdateView):
    form_class = AddBookForm
    success_url = reverse_lazy('viewBooks')
    queryset = Book.objects.all()
    template_name = 'inventory/updateBook.html'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Book, id=id)


@method_decorator(decorators, name='dispatch')
class DeleteBookView(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        book = Book.objects.get(id=id)
        book.delete()
        return redirect('viewBooks')


@method_decorator(decorators, name='dispatch')
class BooksView(View):
    template_name = 'inventory/viewBooks.html'

    def get(self, request, *args, **kwargs):
        context = {}
        form = SearchBookForm()
        books = Book.objects.all()
        context['books'] = books
        context['form'] = form
        return render(request, self.template_name, context)

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
                return render(request, self.template_name, context)

            selected_books = books.filter(**filters)
            if not selected_books:
                context['error'] = 'No Books Found'

            context['books'] = selected_books
            context['form'] = form
            return render(request, self.template_name, context)


@method_decorator(decorators, name='dispatch')
class TagsView(TemplateView):
    template_name = 'inventory/viewTags.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags'] = tags
        return context


@method_decorator(decorators, name='dispatch')
class AddTagView(CreateView):
    form_class = AddTagForm
    success_url = reverse_lazy('viewTags')
    template_name = 'inventory/addTagForm.html'


@method_decorator(decorators, name='dispatch')
class UpdateTagView(UpdateView):
    form_class = AddTagForm
    success_url = reverse_lazy('viewTags')
    template_name = 'inventory/updateBook.html'
    queryset = Tag.objects.all()

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Tag, id=id)


@method_decorator(decorators, name='dispatch')
class DeleteTagView(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        tag = Tag.objects.get(id=id)
        tag.delete()
        return redirect('viewTags')