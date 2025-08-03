from django.shortcuts import render, redirect
from django.contrib import messages
from main_app.models.base_user.user import User
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
import random
import string


def login_with_code_request(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")  # email, username или phone
        user = User.objects.filter(
                email=identifier
            ).first() or User.objects.filter(
                username=identifier
            ).first() or User.objects.filter(
                phone_number=identifier
            ).first()

        if not user:
            messages.error(request, "Пользователь не найден.")
        else:
            code = ''.join(random.choices(string.digits, k=6))
            user.confirmation_code = code
            user.code_created_at = now()
            user.save()

            # Отправка письма
            send_mail(
                "Код входа",
                f"Ваш код для входа: {code}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            # Сохраняем user.id вместо email
            request.session["login_code_user_id"] = user.id
            return redirect("login_code_confirm")

    return render(request, "login_email_cahngepass/login_code_request.html")




from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def login_with_code_confirm(request):
    user_id = request.session.get("login_code_user_id")
    if not user_id:
        return redirect("login_code_request")

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect("login_code_request")

    if request.method == "POST":
        code = request.POST.get("code")
        print(f"Полученный код: {code}, ожидаемый: {user.confirmation_code}")
        if user.confirmation_code == code:
            if user.code_created_at and timezone.now() - user.code_created_at > timedelta(minutes=10):
                messages.error(request, "Код истёк.")
            else:
                user.confirmation_code = None
                user.code_created_at = None
                user.save()

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)  # Без user.backend
                print("✅ Пользователь вошёл. Редирект на home.")
                return redirect("home")
        else:
            messages.error(request, "Неверный код.")


    return render(request, "login_code_confirm.html", {"email": user.email})
