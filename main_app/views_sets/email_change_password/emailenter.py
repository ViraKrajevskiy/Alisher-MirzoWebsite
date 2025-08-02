from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from main_app.views_sets.email_change_password.ChangePasswordemail import send_confirmation_code

User = get_user_model()

def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            send_confirmation_code(user)
            request.session["reset_email"] = email
            return redirect("confirm_code") 
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким email не найден.")
    return render(request, "account/reset_request.html")
