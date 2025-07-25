from django.contrib import admin
from main_app.models.base_user.user import User
from main_app.models.email_forms.email_send import ContactMessage
from main_app.models.model_albums.albums import Album, ComentAlbum
from main_app.models.model_book.book import ComentBook, Book, BookLike,CommentBookLike
from main_app.models.model_news.news import News,Comment,NewsType,CommentLikes,NewsTypeChoices
from main_app.models.model_picture.picture import Picture,CommentPicture , PictureLike,CommentPictureLike
from main_app.models.model_subscribe_news.news_subscribe import NewsSubscriber

# Регистрируем всё
admin.site.register([Album,ComentAlbum,])
admin.site.register([User])
admin.site.register([Book,ComentBook,CommentBookLike,BookLike])
admin.site.register([News,Comment,NewsType,NewsTypeChoices,CommentLikes])
admin.site.register([Picture,CommentPicture,CommentPictureLike,PictureLike])
admin.site.register([NewsSubscriber,ContactMessage])
