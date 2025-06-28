from django.contrib.auth import login, logout
from main_app.forms.login import UsernameOrEmailLoginForm
from random import randint
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from main_app.forms.forms import RegisterForm
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages

def generate_code():
    return str(randint(100000, 999999))

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Генерируем код подтверждения
            code = generate_code()
            request.session['registration_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'phone_number': form.cleaned_data['phone_number'],
                'password': form.cleaned_data['password'],
                'confirmation_code': code,
                'code_created_at': timezone.now().isoformat()
            }

            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {code}',
                'alishermirzowork@gmail.com',
                [form.cleaned_data['email']],
                fail_silently=False,
            )

            return redirect('confirm_email')
    else:
        form = RegisterForm()
    return render(request, 'autorization_account/registration/registration.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Теперь используем 'username' вместо 'username_or_email'
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Или ваш целевой URL
        else:
            # Добавляем ошибку в контекст
            return render(request, 'autorization_account/login/login.html', {
                'form_errors': True
            })

    return render(request, 'autorization_account/login/login.html')
def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'main_page/main_site.html')
