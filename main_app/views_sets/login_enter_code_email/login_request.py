from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import random
import string
from django.contrib.auth import login, get_user_model
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect, render
from django.contrib import messages
from django.template.loader import render_to_string

User = get_user_model()

def send_login_code_email(user, code):
    subject = "Код входа"
    text_content = f"Ваш код для входа: {code}"
    html_content = render_to_string("emails/login_code.html", {"code": code, "user": user})

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def login_with_code_request(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")  # email, username или phone
        user = User.objects.filter(email=identifier).first() \
            or User.objects.filter(username=identifier).first() \
            or User.objects.filter(phone_number=identifier).first()

        if not user:
            messages.error(request, "Пользователь не найден.")
        else:
            code = ''.join(random.choices(string.digits, k=6))
            user.confirmation_code = code
            user.code_created_at = now()
            user.save()

            send_login_code_email(user, code)

            request.session["login_code_user_id"] = user.id
            return redirect("login_code_confirm")

    return render(request, "login_email_cahngepass/login_code_request.html")


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

                login(request, user)
                print("✅ Пользователь вошёл. Редирект на home.")
                return redirect("home")
        else:
            messages.error(request, "Неверный код.")

    return render(request, "login_code_confirm.html", {"email": user.email})
    