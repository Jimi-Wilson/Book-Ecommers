from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name="sHome"),
    path('register', StaffRegister.as_view(), name='sRegister'),
    path('add/book', AddBook.as_view(), name="addBook"),
    path('books', ViewBooks.as_view(), name="viewBooks"),
    path('book/update/<int:id>', UpdateBook.as_view(), name="updateBook"),
    path('book/delete/<int:id>', DeleteBook.as_view(), name="deleteBook"),
    path('add/tag', AddTag.as_view(), name="addTag"),
    path('tags', ViewTags.as_view(), name="viewTags"),
    path('tag/update/<int:id>', UpdateTag.as_view(), name="updateTag"),
    path('tag/delete/<int:id>', DeleteTag.as_view(), name="deleteTag"),
]
