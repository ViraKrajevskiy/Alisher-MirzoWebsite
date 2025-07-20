from main_app.models.model_albums.albums import Album, ComentAlbum
from main_app.models.model_book.book import Book
from main_app.models.model_news.news import News, Comment
from main_app.models.model_picture.picture import Picture
from django.shortcuts import render

from django.shortcuts import get_object_or_404

# NEWS
def news_list(request):
    news_items = News.objects.all()
    return render(request, 'pages_main_news/news.html', {'news_items': news_items})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = Comment.objects.filter(news=news)
    return render(request, 'pages_main_news/news.html', {'news': news, 'comments': comments})






# gallery/ — список
# просмотр галереии
# список картин в странице только для картин
def all_pictures_view(request):
    pictures = Picture.objects.all()# или просто .all() если нет сортировки

    def chunked(queryset, size):
        for i in range(0, len(queryset), size):
            yield queryset[i:i+size]

    pictures_chunks = list(chunked(list(pictures), 90))

    return render(request, 'pages_main_picture/picture_list.html', {'pictures_chunks': pictures_chunks})



# функции основной страницы
# Показ картин в основной странице
def main_page(request):
    pictures = Picture.objects.all()[:15]
    albums = Album.objects.all()[:5]
    books = Book.objects.all()[:3]

    return render(request,'main_page/main_site.html',{'pictures':pictures, 'albums':albums,'books':books})


