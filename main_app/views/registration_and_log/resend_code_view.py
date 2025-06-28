from django.core.mail import send_mail
from main_app.views.registration_and_log.log_registration import generate_code
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone


def resend_code_view(request):
    data = request.session.get('registration_data')
    if not data or not data.get('email'):
        messages.error(request, "Сессия регистрации не найдена.")
        return redirect('register')

    # Генерируем новый код
    new_code = generate_code()

    # Обновляем данные в сессии
    request.session['registration_data'] = {
        **data,
        'confirmation_code': new_code,
        'code_created_at': timezone.now().isoformat()
    }
    request.session.modified = True

    # Отправляем письмо
    try:
        send_mail(
            'Новый код подтверждения',
            f'Ваш новый код подтверждения: {new_code}',
            'alishermirzowork@gmail.com',
            [data['email']],
            fail_silently=False,
        )
        messages.success(request, "Новый код отправлен на ваш email.")
    except Exception as e:
        messages.error(request, f"Ошибка при отправке письма: {str(e)}")
        return redirect('register')

    return redirect('confirm_email')