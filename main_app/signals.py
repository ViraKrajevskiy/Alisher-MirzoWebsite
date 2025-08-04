from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import News, NewsSubscriber  # путь к моделям должен быть корректным

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import News, NewsSubscriber

@receiver(post_save, sender=News)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = NewsSubscriber.objects.select_related('user').all()
        for subscriber in subscribers:
            send_mail(
                subject=f"📰 Новая новость: {instance.title}",
                message=instance.main_text[:500] + '...',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.user.email],
                fail_silently=True
            )
            