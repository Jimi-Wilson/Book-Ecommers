from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('books', BooksView.as_view(), name='books'),
    path('book/<int:id>', BookView.as_view(), name='book'),
]
