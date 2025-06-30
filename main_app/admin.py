from django.contrib import admin
from main_app.models.base_user.user import User
from main_app.models.model_albums.albums import Album, ComentAlbum
from main_app.models.model_book.book import ComentBook, Book
from main_app.models.model_news.news import News,Comment
from main_app.models.model_picture.picture import Picture,CommentPicture


# Регистрируем всё
admin.site.register([Album,ComentAlbum])
admin.site.register([User])
admin.site.register([Book,ComentBook])
admin.site.register([News,Comment])
admin.site.register([Picture,CommentPicture])

