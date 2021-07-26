from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('register', staff_register, name='sRegister'),
    path('add-book', add_book, name="addBook"),
    path('books', view_books, name="viewBooks"),
    path('book/update/<int:id>', update_book, name="updateBook"),
]
