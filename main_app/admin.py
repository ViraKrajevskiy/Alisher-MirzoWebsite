from django.contrib import admin
from main_app.models.base_user.user import User
from main_app.models.email_forms.email_send import ContactMessage
from main_app.models.model_albums.albums import Album, ComentAlbum
from main_app.models.model_book.book import ComentBook, Book
from main_app.models.model_news.news import News,Comment,NewsType
from main_app.models.model_picture.picture import Picture,CommentPicture
from main_app.models.model_subscribe_news.news_subscribe import NewsSubscriber

admin.site.register([Album,ComentAlbum,News,Comment,NewsType,Book,ComentBook,User,Picture,CommentPicture,NewsSubscriber,ContactMessage])
