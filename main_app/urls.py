from django.urls import path

from main_app.views.print_filter_obj.main_filter_print import (
    news_detail, news_list, album_detail, album_list, main_page, all_pictures_view
)
from main_app.views.registration_and_log.log_registration import (
    login_view, register_view, logout_view
)
from main_app.views.registration_and_log.confirm_email_view import confirm_email_view
from main_app.views.registration_and_log.resend_code_view import resend_code_view
from main_app.views_sets.Books.books import (
    like_comment, like_book, delete_comment, update_comment, book_list, add_comment
)
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
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),  # 🆕
    path('comments/<int:comment_id>/update/', update_comment, name='update_comment'),  # 🆕

    # Альбомы
    path('albums/', album_list, name='album_list'),
    path('albums/<int:pk>/', album_detail, name='album_detail'),

    # Новости
    path('news/', news_list, name='news_list'),
    path('news/<int:pk>/', news_detail, name='news_detail'),

    # Картины
    path('all-pictures/', all_pictures_view, name='all_pictures'),
]
