from django.shortcuts import redirect, render
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages
from main_app.models.base_user.user import User
from django.contrib.auth import update_session_auth_hash, login

def confirm_code_and_reset_password(request):
    email = request.session.get("reset_email")
    if not email:
        return redirect("request_password_reset")

    if request.method == "POST":
        code = request.POST.get("code")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email, confirmation_code=code)
            if user.code_created_at and now() - user.code_created_at > timedelta(minutes=10):
                messages.error(request, "Код истёк.")
            else:
                user.set_password(password)
                user.confirmation_code = None
                user.code_created_at = None
                user.save()

                # 🔒 Указать backend вручную
                user.backend = 'main_app.backends.UsernameOrEmailBackend'

                # 🔑 Авторизуем пользователя заново
                login(request, user)

                # 🔁 Обновить сессию, если был авторизован
                update_session_auth_hash(request, user)

                messages.success(request, "Пароль успешно изменён.")
                return redirect("account")
        except User.DoesNotExist:
            messages.error(request, "Неверный код.")
    return render(request, "account/confirm_code.html")
