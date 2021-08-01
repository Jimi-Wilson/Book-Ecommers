from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name="sHome"),
    path('register', StaffRegisterView.as_view(), name='sRegister'),
    path('add/book', AddBookView.as_view(), name="addBook"),
    path('books', BooksView.as_view(), name="viewBooks"),
    path('book/update/<int:id>', UpdateBookView.as_view(), name="updateBook"),
    path('book/delete/<int:id>', DeleteBookView.as_view(), name="deleteBook"),
    path('add/tag', AddTagView.as_view(), name="addTag"),
    path('tags', TagsView.as_view(), name="viewTags"),
    path('tag/update/<int:id>', UpdateTagView.as_view(), name="updateTag"),
    path('tag/delete/<int:id>', DeleteTagView.as_view(), name="deleteTag"),
]
