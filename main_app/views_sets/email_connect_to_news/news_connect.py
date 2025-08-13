from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from main_app.views.services import SubscriptionService
from main_app.models.model_news.news import NewsSubscriber, NewsType



def subscribe_to_news(request):
    if request.method != "POST":
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Получаем данные из формы
    news_type_id = request.POST.get("news_type_id") or None
    email = request.POST.get("email", "").strip()

    # Приводим news_type_id к int или None
    if news_type_id:
        try:
            news_type_id = int(news_type_id)
        except ValueError:
            messages.error(request, "Неверный тип новости.")
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        news_type_id = None  # Все новости

    if request.user.is_authenticated:
        # Если авторизован — email из профиля и сразу confirmed=True
        subscriber, created = NewsSubscriber.objects.get_or_create(
            user=request.user,
            news_type_id=news_type_id,
            defaults={
                "email": request.user.email,
                "confirmed": True
            }
        )
    else:
        # Гость должен ввести email
        if not email:
            messages.error(request, "Email обязателен для подписки.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        subscriber, created = NewsSubscriber.objects.get_or_create(
            email=email,
            news_type_id=news_type_id,
            defaults={"confirmed": False}
        )

    if created:
        messages.success(request, "Вы успешно подписаны на новости!")
    else:
        messages.info(request, "Вы уже подписаны на выбранные новости.")

    return redirect(request.META.get("HTTP_REFERER", "/"))

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
