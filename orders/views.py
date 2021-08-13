from django.shortcuts import render
from django.views import View
from Inventory.models import Order, OrderItem


class MyOrdersView(View):
    template_name = 'orders/myOrders.html'

    def get(self, request, *args, **kwargs):
        context = {}
        orders = Order.objects.all().filter(user=request.user,
                                            payment_complete=True)
        context['orders'] = orders

        return render(request, self.template_name, context)