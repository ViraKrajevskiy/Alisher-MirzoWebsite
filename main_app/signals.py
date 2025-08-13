from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from main_app.models.model_news.news import NewsSubscriber, News

@receiver(post_save, sender=News)
def send_news_to_subscribers(sender, instance, created, **kwargs):
    if not created:
        return  # отправляем только при создании новой новости

    # Берем только активных и подтвержденных подписчиков с email
    subscribers = NewsSubscriber.objects.filter(is_active=True, confirmed=True).exclude(email__isnull=True).exclude(email='')

    # Ссылка на страницу всех новостей
    site_url = getattr(settings, "SITE_URL", "http://164.92.252.126/news/")

    news_type_name = instance.type.name if instance.type else "Все новости"

    for sub in subscribers:
        try:
            send_mail(
                subject=f"[{news_type_name}] Новая новость: {instance.title}",
                message=(
                    f"Здравствуйте!\n\n"
                    f"Новая новость ({news_type_name}): {instance.title}\n\n"
                    f"Посмотреть на сайте: {site_url}\n\n"
                    f"Спасибо, что с нами!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[sub.email],
                fail_silently=False  # ошибки будут видны в логах
            )
        except Exception as e:
            print(f"Ошибка при отправке письма {sub.email}: {e}")
            