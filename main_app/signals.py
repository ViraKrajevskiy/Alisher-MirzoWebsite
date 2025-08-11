from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from main_app.models.model_news.news import NewsSubscriber,News


@receiver(post_save, sender=News)
def send_news_to_subscribers(sender, instance, created, **kwargs):
    if created:  # новость только что создана
        subject = f"Новая новость: {instance.title}"
        message = f"{instance.main_text[:300]}...\n\nПодробнее: {settings.SITE_URL}/news/{instance.id}/"

        # собираем список email
        emails = []
        for sub in NewsSubscriber.objects.all():
            if sub.user and sub.user.email:
                emails.append(sub.user.email)
            elif sub.email:
                emails.append(sub.email)

        # убираем дубликаты
        emails = list(set(emails))

        if emails:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                emails,
                fail_silently=False,
            )