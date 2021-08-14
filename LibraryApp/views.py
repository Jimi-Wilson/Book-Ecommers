from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView
from Inventory.models import Book, Order, OrderItem
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views import View
from .forms import *
import stripe
from Library import settings

# Create your views here.


# Returns home template
class HomeView(TemplateView):
    template_name = 'library/home.html'


class BooksView(View):
    template_name = 'library/books.html'
    books = Book.objects.all()

    def get(self, request, *args,
            **kwargs):  # Gets all books and passes them to context
        context = {'books': self.books}

        f_form = FilterForm()
        context['f_form'] = f_form

        form = SearchForm()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        filters = {}
        count = 0

        form = SearchForm(request.POST)
        context['form'] = form
        f_form = FilterForm()
        context['f_form'] = f_form

        try:
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

            selected_books = self.books.filter(**filters)
            context['books'] = selected_books

        except AttributeError:
            if f_form := FilterForm(request.POST):
                context['f_form'] = f_form

                tags = f_form['tags'].value()
                if tags:
                    selected_books = set(self.books.filter(tags__in=tags))
                    context['books'] = selected_books
                    context['f_form'] = f_form
                    return render(request, self.template_name, context)

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


@method_decorator(login_required, name='dispatch')
class AddItemToCartView(View):
    template_name = 'library/addItem.html'

    def get(self, request, *args, **kwargs):

        order = Order.objects.all()
        order = Order.objects.filter(user=request.user,
                                     payment_complete=False).first()

        if not order:
            order = Order(user=request.user,
                          transaction_id=Order.transaction_id_gen())
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


@method_decorator(login_required, name='dispatch')
class CartView(View):
    template_name = 'library/cart.html'

    def get(self, request, *args, **kwargs):
        context = {}
        order = Order.objects.filter(user=request.user, payment_complete=False)
        order = order.filter(user=request.user).first()
        print(order)
        context['order'] = order
        order_items = OrderItem.objects.filter(order=order)
        context['order_items'] = order_items
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CartItemDeleteView(View):
    def get(self, request, *args, **kwargs):
        order_item_id = kwargs.get('id')
        order_items = OrderItem.objects.filter(id=order_item_id)
        order_items.delete()
        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class CartQuantityUpdateView(UpdateView):
    form_class = CartQuantityForm
    success_url = reverse_lazy('cart')
    template_name = 'library/updateQuantity.html'
    queryset = OrderItem.objects.all()

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(OrderItem, id=id)


@method_decorator(login_required, name='dispatch')
class ShippingAddressView(View):
    template_name = 'library/shipping.html'
    form = ShippingAddressForm

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.form

        order = Order.objects.filter(user=request.user,
                                     payment_complete=False).first()

        if request.user.shipping_address:
            order.shipping_address = request.user.shipping_address
            return redirect('checkout')
        context['order'] = order
        order_items = OrderItem.objects.filter(order=order)
        context['order_items'] = order_items
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        order = Order.objects.all()
        order = Order.objects.filter(user=request.user,
                                     payment_complete=False).first()
        form = ShippingAddressForm(request.POST)

        if form.is_valid():

            shipping_address = form.save()
            order.shipping_address = shipping_address
            order.save()

            request.user.shipping_address = shipping_address
            request.user.save()
            return redirect('checkout')

        context['form'] = form
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    post_template = 'templates/'

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user,
                                     payment_complete=False).first()

        if shipping_address := request.user.shipping_address:
            order.shipping_address = shipping_address

        elif order.shipping_address == None:
            return redirect('shipping')

        order_items = OrderItem.objects.all().filter(order=order)
        line_items = []
        item = {}

        for i in order_items:
            item['price'] = i.product.payment_id
            item['quantity'] = i.quantity
            line_items.append(item)
            item = {}

        stripe.api_key = settings.STRIPE_API_KEY

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=[
                'card',
            ],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart/checkout/success',
            cancel_url='http://127.0.0.1:8000/cart/checkout/cancel',
        )
        return redirect(checkout_session.url)


@method_decorator(login_required, name='dispatch')
class CheckoutSuccessView(View):
    template_name = 'payment/success.html'

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user,
                                     payment_complete=False).first()
        order.payment_complete = True
        order.save()
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class CheckoutCancelView(View):
    template_name = 'payment/cancel.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
