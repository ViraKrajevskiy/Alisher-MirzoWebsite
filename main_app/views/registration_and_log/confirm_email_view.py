from django.utils.dateparse import parse_datetime
from datetime import timedelta
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

User = get_user_model()
def confirm_email_view(request):
    data = request.session.get('registration_data')
    if not data:
        messages.error(request, "Сессия регистрации не найдена или истекла.")
        return redirect('register')

    if request.method == 'POST':
        code_input = request.POST.get('code')
        if not code_input:
            messages.error(request, "Введите код подтверждения")
            return redirect('confirm_email')

        # Проверяем код и время
        if code_input != data['confirmation_code']:
            messages.error(request, "Неверный код подтверждения")
            return redirect('confirm_email')

        code_created_at = parse_datetime(data['code_created_at'])
        if timezone.now() - code_created_at > timedelta(minutes=5):
            messages.error(request, "Срок действия кода истёк. Запросите новый.")
            return redirect('resend_code')

        # Создаём пользователя
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                phone_number=data['phone_number'],
                password=data['password'],
                is_active=True  # Активируем сразу после подтверждения
            )
            # Очищаем сессию
            request.session.pop('registration_data', None)
            messages.success(request, "Регистрация успешно завершена! Теперь вы можете войти.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Ошибка при создании пользователя: {str(e)}")
            return redirect('register')

    return render(request, 'autorization_account/registration/confirmCode.html', {
        'email': data['email'][:3] + '***' + data['email'].split('@')[-1]  # Маскируем email для показа
    })