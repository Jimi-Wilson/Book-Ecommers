from django.http import request
from django.template import response
from django.template.response import ContentNotRenderedError
from Inventory.models import Book, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views import View
from .forms import *

# Create your views here.


# Returns home template
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'library/home.html'


class BooksView(View):
    template_name = 'library/books.html'
    books = Book.objects.all()

    def get(self, request, *args,
            **kwargs):  # Gets all books and passes them to context
        context = {}

        context['books'] = self.books

        form = SearchForm()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        filters = {}
        count = 0

        form = SearchForm(request.POST)
        context['form'] = form

        search_field = form['search_field'].value().strip()

        if self.books.filter(title__icontains=search_field).count() > 0:
            filters['title__icontains'] = search_field
            count = +1

        if self.books.filter(author__icontains=search_field).count() > 0:
            filters['author__icontains'] = search_field
            count = +1

        if count == 0:
            context['search_error'] = True
            context['search_field'] = search_field
            return render(request, self.template_name, context)

        books = self.books.filter(**filters)
        context['books'] = books
        return render(request, self.template_name, context)


class BookView(TemplateView):
    template_name = 'library/book.html'

    def get_context_data(
            self, **kwargs):  # Gets tags and book and passes them to context
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('id')
        book = Book.objects.get(id=id)

        tags = book.tags
        tags = [i.name for i in tags.all()]

        context['tags'] = tags
        context['book'] = book
        return context


class AddItemToCartView(View):
    template_name = 'library/addItem.html'

    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        order = Order.objects.filter(user=request.user, complete=False).first()
        if not order:
            order = Order(user=request.user,
                          complete=False,
                          trasaction_id="egjipijrgwirgjeorgeijogreoikj")
            order.save()

        book_id = self.kwargs.get('id')
        book = Book.objects.get(id=book_id)
        if OrderItem.objects.filter(product=book, order=order):

            order_item = OrderItem.objects.filter(product=book,
                                                  order=order).first()
            order_item.quantity = order_item.quantity + 1
            print(order_item.quantity)
            order_item.save()
            return render(request, self.template_name)

        else:
            order_items = OrderItem(product=book, order=order, quantity=+1)
            order_items.save()
            print(order.get_cart_total)
            return render(request, self.template_name)


class CartView(View):
    template_name = 'library/cart.html'

    def get(self, request, *args, **kwargs):
        context = {}
        order = Order.objects.filter(user=request.user, complete=False).first()
        order_items = OrderItem.objects.filter(order=order)
        context['order_items'] = order_items
        return render(request, self.template_name, context)
