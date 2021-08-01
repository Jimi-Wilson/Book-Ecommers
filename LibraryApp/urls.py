from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('books', BooksView.as_view(), name='books'),
    path('book/<int:id>', BookView.as_view(), name='book'),
    path('add-item/<int:id>', AddItemToCartView.as_view(), name='addItem'),
    path('cart', CartView.as_view(), name='cart')
]
