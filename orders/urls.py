from .views import *
from django.urls import path, include

urlpatterns = [
    path('myorders/', MyOrdersView.as_view(), name='myOrders'),
]
