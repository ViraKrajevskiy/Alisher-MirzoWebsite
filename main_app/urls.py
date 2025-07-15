from django.urls import path

from main_app.views.print_filter_obj.main_filter_print import book_list, news_detail, \
    news_list, album_detail, album_list, book_detail, main_page, all_pictures_view
from main_app.views.registration_and_log.log_registration import login_view, register_view, logout_view
from main_app.views.registration_and_log.confirm_email_view import confirm_email_view
from main_app.views.registration_and_log.resend_code_view import resend_code_view


from main_app.views_sets.contact_view.contact_view_message import contact_view
from main_app.views_sets.email_connect_to_news.news_connect import subscribe_to_news

urlpatterns = [
    path('', main_page, name='home'),

    path('contact/', contact_view, name='contact'),
    path('subscribe/', subscribe_to_news, name='subscribe_to_news'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('confirm-email/', confirm_email_view, name='confirm_email'),
    path('resend-code/', resend_code_view, name='resend_code'),

    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),

    path('albums/', album_list, name='album_list'),
    path('albums/<int:pk>/', album_detail, name='album_detail'),

    path('news/', news_list, name='news_list'),
    path('news/<int:pk>/', news_detail, name='news_detail'),

    # Картины страницы показ данных
    path('all-pictures/', all_pictures_view, name='all_pictures'),
]
