
from django.shortcuts import render, get_object_or_404

from main_app.models.model_albums.albums import Album, ComentAlbum
from main_app.models.model_book.book import Book, ComentBook
from main_app.models.model_news.news import News, Comment
from main_app.models.model_picture.picture import Picture, CommentPicture
from django.shortcuts import render
from collections import defaultdict


def main_page(request):
    featured_artworks = Picture.objects.all()
    return render(request, 'main_page/main_site.html', {'featured_artworks': featured_artworks})

# BOOK
def book_list(request):
    books = Book.objects.all()
    return render(request, 'main_pages_books/book..html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = ComentBook.objects.filter(books=book)
    return render(request, 'main_pages_books/book.html', {'book': book, 'comments': comments})


# ALBUM
def album_list(request):
    albums = Album.objects.all()
    return render(request, 'pages_main_albums/albums.html', {'albums': albums})

def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    comments = ComentAlbum.objects.filter(album=album)
    return render(request, 'pages_main_albums/albums.html', {'album': album, 'comments': comments})


# NEWS
def news_list(request):
    news_items = News.objects.all()
    return render(request, 'pages_main_news/news.html', {'news_items': news_items})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = Comment.objects.filter(news=news)
    return render(request, 'pages_main_news/news.html', {'news': news, 'comments': comments})


# PICTURE
# views.py


# gallery/ — список
def all_pictures_view(request):
    pictures = Picture.objects.all().order_by('-date_made')  # или просто .all() если нет сортировки
    return render(request, 'pages_main_picture/picture_list.html', {'pictures': pictures})

