from Inventory.models import Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

# Create your views here.


# Returns home template
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'library/home.html'


# Gets all books and returns template and context
class BooksView(TemplateView):
    template_name = 'library/books.html'

    def get_context_data(
            self, **kwargs):  # Gets all books and passes them to context
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        context['books'] = books
        return context


class BookView(TemplateView):
    template_name = 'library/book.html'

    def get_context_data(
            self, **kwargs):  # Gets tags and book and passes them to context
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('id')
        book = Book.objects.get(id=id)

        tags = book.tags
        tags = [i.name for i in tags.all()]

        context['tags'] = tags
        context['book'] = book
        return context