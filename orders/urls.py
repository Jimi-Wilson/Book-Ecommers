from .views import *
from django.urls import path, include

urlpatterns = [
    path('myorders/', MyOrdersView.as_view(), name='myOrders'),
    path('user/order/<int:id>', DetailOrderView.as_view(), name='userorder'),
    path('staff/orders', OrdersView.as_view(), name='orders'),
    path('staff/order/<int:id>', DetailOrderView.as_view(), name='order'),
    path('staff/order/update/<int:id>',
         UpdateOrderStatus.as_view(),
         name='order_update')
]
