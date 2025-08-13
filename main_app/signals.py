from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from main_app.models.model_news.news import NewsSubscriber, News

@receiver(post_save, sender=News)
def send_news_to_subscribers(sender, instance, created, **kwargs):
    if not created:
        return

    subscribers = NewsSubscriber.objects.filter(is_active=True, confirmed=True)

    site_url = getattr(settings, "SITE_URL", "http://164.92.252.126")
    news_url = reverse("news_detail", args=[instance.pk])
    full_url = f"{site_url}{news_url}"

    for sub in subscribers:
        send_mail(
            subject=f"[{instance.type}] Новая новость: {instance.title}",
            message=f"Здравствуйте!\n\nНовая новость ({instance.type}): {instance.title}\n\nПодробнее: {full_url}\n\nСпасибо, что с нами!",
            from_email="noreply@example.com",
            recipient_list=[sub.email],
        )
        