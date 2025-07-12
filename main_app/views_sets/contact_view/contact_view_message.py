from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def contact_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        email = request.user.email

        if subject and message:
            try:
                send_mail(
                    f"Вопрос от {request.user.username}: {subject}",
                    message,
                    email,
                    ['alishermirzowork@gmail.com'],  # адрес, куда приходят вопросы
                    fail_silently=False,
                )
                messages.success(request, "Сообщение успешно отправлено.")
            except Exception as e:
                messages.error(request, f"Ошибка при отправке: {e}")
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")

    return redirect('home')  # можно изменить на нужный URL
    