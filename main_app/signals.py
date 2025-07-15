from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import News, NewsSubscriber  # путь к моделям должен быть корректным

@receiver(post_save, sender=News)
def notify_subscribers_on_news_created(sender, instance, created, **kwargs):
    if not created:
        return  # Только при создании

    subject = f"📰 Новая новость: {instance.title}"
    preview = instance.main_text[:250].strip() + "..." if len(instance.main_text) > 250 else instance.main_text
    link = "https://example.com/"  # TODO: Замени на реальный путь к новости
    message = f"{preview}\n\nЧитать полностью: {link}"

    from_email = settings.DEFAULT_FROM_EMAIL

    # Получаем все email-адреса подписчиков
    emails = NewsSubscriber.objects.values_list('email', flat=True)

    # Рассылаем письма
    for email in emails:
        send_mail(
            subject,
            message,
            from_email,
            [email],
            fail_silently=True
        )
        