from django.urls import path

from main_app.views.print_filter_obj.main_filter_print import (
    main_page
)
from main_app.views.registration_and_log.log_registration import (
    login_view, register_view, logout_view
)
from main_app.views.registration_and_log.confirm_email_view import confirm_email_view
from main_app.views.registration_and_log.resend_code_view import resend_code_view
from main_app.views_sets.Albums.albums import add_comment_album,  like_album,  \
     album_list, like_comment_album, update_comment_album, delete_comment_album
from main_app.views_sets.Books.books import (
    like_comment, like_book, delete_comment, update_comment, book_list, add_comment
)
from main_app.views_sets.News.newses import add_comment_news, delete_comment_news, update_comment_news, like_news, \
    like_comment_news, news_list
from main_app.views_sets.Pictures_crud.picture import update_comment_picture, delete_comment_picture, \
    like_comment_picture, add_comment_picture, like_picture, picture_list
from main_app.views_sets.contact_view.contact_view_message import contact_view
from main_app.views_sets.email_connect_to_news.news_connect import subscribe_to_news

urlpatterns = [
    path('', main_page, name='home'),

    # Контакты и подписка
    path('contact/', contact_view, name='contact'),
    path('subscribe/', subscribe_to_news, name='subscribe_to_news'),

    # Аутентификация
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('confirm-email/', confirm_email_view, name='confirm_email'),
    path('resend-code/', resend_code_view, name='resend_code'),

    # Книги
    path('books/', book_list, name='book_list'),
    path('books/<int:book_id>/like/', like_book, name='like_book'),
    path('books/<int:book_id>/add-comment/', add_comment, name='add_comment'),
    path('comments/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('comments/<int:comment_id>/update/', update_comment, name='update_comment'),

    # Альбомы
    path('albums/', album_list, name='album_list'),
    path('albums/<int:album_id>/add-comment/', add_comment_album, name='add_comment_album'),
    path('albums/comment/<int:comment_id>/delete/', delete_comment_album, name='delete_comment_album'),
    path('albums/comment/<int:comment_id>/update/', update_comment_album, name='update_comment_album'),
    path('albums/<int:album_id>/like/', like_album, name='like_album'),
    path('albums/comment/<int:comment_id>/like/', like_comment_album, name='like_comment_album'),


    # Новости
    path('news/', news_list, name='news_list'),
    path('news/<int:news_id>/comment/add/', add_comment_news, name='add_comment_news'),
    path('news/comment/<int:comment_id>/delete/', delete_comment_news, name='delete_comment_news'),
    path('news/comment/<int:comment_id>/edit/', update_comment_news, name='update_comment_news'),
    path('news/<int:news_id>/like/', like_news, name='like_news'),
    path('news/comment/<int:comment_id>/like/', like_comment_news, name='like_comment_news'),

    # Картины
    path('picture/', picture_list, name='picture_list'),
    path('picture/<int:picture_id>/comment/add/', add_comment_picture, name='add_comment_picture'),
    path('picture/comment/<int:comment_id>/delete/', delete_comment_picture, name='delete_comment_picture'),
    path('picture/comment/<int:comment_id>/update/', update_comment_picture, name='update_comment_picture'),
    path('picture/<int:picture_id>/like/', like_picture, name='like_picture'),

    path('picture/comment/<int:comment_id>/like/', like_comment_picture, name='like_comment_picture'),
]
