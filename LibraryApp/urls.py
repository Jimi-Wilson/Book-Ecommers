from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('books', BooksView.as_view(), name='books'),
    path('book/<int:id>', BookView.as_view(), name='book'),
    path('cart/additem/<int:id>', AddItemToCartView.as_view(), name='addItem'),
    path('cart', CartView.as_view(), name='cart'),
    path('cart/delete/<int:id>',
         CartItemDeleteView.as_view(),
         name='deleteItem'),
    path('cart/quantity/<int:id>',
         CartQuantityUpdateView.as_view(),
         name='cartQuantityUpdate'),
    path('cart/checkout', CheckoutView.as_view(), name='checkout'),
    path('cart/add-shipping-address',
         ShippingAddressView.as_view(),
         name='shipping'),
    path('cart/add-billing-address',
         BillingAddressView.as_view(),
         name='billing'),
]
