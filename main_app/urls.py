from django.urls import path

from main_app.views.registration_and_log.log_registration import home_view, login_view, register_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
