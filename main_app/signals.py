from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from main_app.models.model_news.news import NewsSubscriber, News


@receiver(post_save, sender=News)
def send_news_to_subscribers(sender, instance, created, **kwargs):
    if not created:
        return

    subscribers = NewsSubscriber.objects.filter(is_active=True, confirmed=True)

    # Ссылка на страницу всех новостей
    site_url = getattr(settings, "Alisher_MirzoWebsite", "http://164.92.252.126/news/")

    for sub in subscribers:
        send_mail(
            subject=f"[{instance.type}] Новая новость: {instance.title}",
            message=(
                f"Здравствуйте!\n\n"
                f"Новая новость ({instance.type}): {instance.title}\n\n"
                f"Посмотреть на сайте: {site_url}\n\n"
                f"Спасибо, что с нами!"
            ),
            from_email="noreply@example.com",
            recipient_list=[sub.email],
        )
        