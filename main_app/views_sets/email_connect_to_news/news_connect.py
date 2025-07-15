from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from main_app.models import NewsSubscriber

def subscribe_to_news(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        honeypot = request.POST.get('website')  # для защиты от ботов

        if honeypot:
            return redirect('home')  # бот, выходим

        if email and not NewsSubscriber.objects.filter(email=email).exists():
            NewsSubscriber.objects.create(email=email)

            # Отправка письма
            send_mail(
                subject='Подписка на новости',
                message='Спасибо за подписку! Вы будете получать обновления на ваш email.',
                from_email=None,  # или укажи DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, 'Вы успешно подписались на новости!')
        else:
            messages.info(request, 'Вы уже подписаны на новости.')

    return redirect('home')
    