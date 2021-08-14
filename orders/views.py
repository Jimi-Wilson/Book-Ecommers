from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from Inventory.models import Order, OrderItem


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