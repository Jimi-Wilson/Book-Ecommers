from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('register', staffRegister, name='sRegister'),
    path('add-book', addBook, name="addBook")
]
