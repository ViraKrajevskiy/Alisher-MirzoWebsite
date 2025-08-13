from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from main_app.views.services import SubscriptionService
from main_app.models.model_news.news import NewsType
from django.db.models import Q
from django.utils import timezone

@require_POST
def subscribe_to_news(request):
    """
    Обычная форма подписки (без AJAX).
    """
    email = request.POST.get('email') if not request.user.is_authenticated else None
    user = request.user if request.user.is_authenticated else None
    news_type = request.POST.get('news_type')
    all_types = request.POST.get('all_types') == 'on'

    # Honeypot проверка
    if request.POST.get('website'):
        messages.warning(request, "Подозрительная активность, подписка не оформлена")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    # Проверка типа новости
    if news_type and not NewsType.objects.filter(pk=news_type).exists():
        messages.error(request, "Неверный тип новости")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    try:
        _, _, confirmation_sent = SubscriptionService.subscribe(
            email=email,
            user=user,
            news_type_id=None if all_types else news_type
        )

        if confirmation_sent:
            messages.success(request, "Проверьте ваш email для подтверждения подписки")
        else:
            messages.success(request, "Вы успешно подписались на новости")

    except Exception as e:
        messages.error(request, str(e))

    return redirect(request.META.get('HTTP_REFERER', 'home'))

# views.py
from django.shortcuts import redirect
from django.contrib import messages


def subscribe_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        news_type_id = request.POST.get("news_type_id")
        user = request.user if request.user.is_authenticated else None

        subscriber, created, confirmation_sent = SubscriptionService.subscribe(
            email=email,
            user=user,
            news_type_id=news_type_id
        )

        if created:
            if confirmation_sent:
                messages.success(request, "Подтвердите подписку по ссылке в письме.")
            else:
                messages.success(request, "Вы подписаны на новости.")
        else:
            messages.info(request, "Вы уже подписаны.")

    return redirect(request.META.get("HTTP_REFERER", "/"))





@login_required
@require_POST
def unsubscribe_from_news(request):
    """
Обычная форма отписки (без AJAX).
    """
    news_type = request.POST.get('news_type')

    try:
        SubscriptionService.unsubscribe(
            user=request.user,
            news_type_id=news_type
        )
        messages.success(request, "Вы успешно отписались от рассылки")

    except Exception as e:
        messages.error(request, str(e))

    return redirect(request.META.get('HTTP_REFERER', 'home'))
