from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from Inventory.models import Order, OrderItem
from Inventory.decorators import is_staff

decorators = [login_required, is_staff]


@method_decorator(login_required, name='dispatch')
class MyOrdersView(View):
    template_name = 'orders/myOrders.html'

    def get(self, request, *args, **kwargs):
        context = {}
        orders = Order.objects.all().filter(user=request.user,
                                            payment_complete=True)
        context['orders'] = orders

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class DetailOrderView(View):
    template_name = 'orders/orders.html'

    def get(self, request, id, *args, **kwargs):
        context = {}

        order = Order.objects.get(id=id)
        context['order'] = order
        order_items = OrderItem.objects.all().filter(order=order)
        context['order_items'] = order_items
        return render(request, self.template_name, context)


@method_decorator(decorators, name='dispatch')
class OrdersView(View):
    template_name = 'orders/staff_orders.html'

    def get(self, request, *args, **kwargs):
        context = {}
        orders = Order.objects.all().filter(payment_complete=True)
        context['orders'] = orders
        return render(request, self.template_name, context)


@method_decorator(decorators, name='dispatch')
class StaffDetailOrderView(View):
    template_name = 'orders/staff_order.html'

    def get(self, request, id, *args, **kwargs):
        context = {}
        order = Order.objects.get(id=id)
        order_items = OrderItem.objects.all().filter(order=order)
        context['order_items'] = order_items
        context['order'] = order
        return render(request, self.template_name, context)


@method_decorator(decorators, name='dispatch')
class UpdateOrderStatus(UpdateView):
    model = Order
    fields = ['complete']
    template_name = 'orders/update.html'
    success_url = reverse_lazy('sHome')

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Order, id=id)