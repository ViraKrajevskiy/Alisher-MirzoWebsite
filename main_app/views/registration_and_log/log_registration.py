# main_app/views/registration_and_log.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from main_app.forms.forms import RegisterForm
from main_app.forms.login import UsernameOrEmailLoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'autorization_account/registration/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UsernameOrEmailLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UsernameOrEmailLoginForm()
    return render(request, 'autorization_account/login/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'main_page/main_site.html')
