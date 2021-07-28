from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="sHome"),
    path('register', staff_register, name='sRegister'),#

    path('add/book', add_book, name="addBook"),
    path('books', view_books, name="viewBooks"),
    path('book/update/<int:id>', update_book, name="updateBook"),
    path('book/delete/<int:id>', delete_book, name="deleteBook"),


    path('add/tag', add_tag, name="addTag"),
    path('tags', view_tags, name="viewTags"),
    path('tag/update/<int:id>', update_tag, name="updateTag"),
    path('tag/delete/<int:id>', delete_tag, name="deleteTag"),


]





