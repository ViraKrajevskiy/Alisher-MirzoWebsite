from django.shortcuts import render, get_object_or_404, redirect

from main_app.models.model_book.book import Book


# Список
def book_list(request):
    books = Book.objects.all()
    return render(request, 'dashboard/home.html', {'books': books})


