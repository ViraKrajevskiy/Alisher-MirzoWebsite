from main_app.models.model_albums.albums import Album, ComentAlbum
from main_app.models.model_book.book import Book
from main_app.models.model_news.news import News, Comment
from main_app.models.model_picture.picture import Picture
from django.shortcuts import render

from django.shortcuts import get_object_or_404

# функции основной страницы
# Показ картин в основной странице
def main_page(request):
    pictures = Picture.objects.all()[:15]
    albums = Album.objects.all()[:5]
    books = Book.objects.all()[:3]

    return render(request,'main_page/main_site.html',{'pictures':pictures, 'albums':albums,'books':books})


