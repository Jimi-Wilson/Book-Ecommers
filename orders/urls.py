from .views import *
from django.urls import path, include

urlpatterns = [
    path('myorders/', MyOrdersView.as_view(), name='myOrders'),
    path('order/<int:id>', DetailOrderView.as_view(), name='order'),
]
