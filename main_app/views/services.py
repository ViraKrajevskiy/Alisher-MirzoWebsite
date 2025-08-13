# services.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.db import models
import logging

from main_app.models.model_news.news import NewsType, NewsSubscriber

logger = logging.getLogger(__name__)

class SubscriptionService:
    @staticmethod
    def subscribe(email=None, user=None, news_type_id=None):
        """
Подписка пользователя или email на новости
:param email: Для анонимной подписки
:param user: Для авторизованных пользователей
:param news_type_id: ID типа новостей (None для всех)
:return: (subscriber, created, confirmation_sent)
        """
        if not email and not user:
            raise ValueError("Требуется email или пользователь")

        news_type = None
        if news_type_id:
            try:
                news_type = NewsType.objects.get(pk=news_type_id)
            except NewsType.DoesNotExist:
                logger.warning(f"NewsType {news_type_id} не найден")

        subscriber, created = NewsSubscriber.objects.get_or_create(
            **{'user': user} if user else {'email': email},
            news_type=news_type,
            defaults={'is_active': not bool(email)}  # Для email требуется подтверждение
        )

        confirmation_sent = False
        if created and email:
            SubscriptionService.send_confirmation_email(subscriber)
            confirmation_sent = True

        return subscriber, created, confirmation_sent

    @staticmethod
    def send_confirmation_email(subscriber):
        """Отправка email с подтверждением подписки"""
        if not subscriber.email:
            return False

        context = {
            'confirmation_url': (
                f"https://ваш-сайт.ru/confirm-subscription/"
                f"?token={subscriber.confirmation_token}"
            ),
            'days_valid': 10,
            'news_type': subscriber.news_type.name if subscriber.news_type else "все новости"
        }

        subject = "Подтвердите подписку на новости"
        message = render_to_string('emails/subscription_confirmation.txt', context)
        html_message = render_to_string('emails/subscription_confirmation.html', context)

        try:
            send_mail(
                subject,
                message,
                'noreply@ваш-сайт.ru',
                [subscriber.email],
                html_message=html_message
            )
            return True
        except Exception as e:
            logger.error(f"Ошибка отправки email: {e}")
            return False

    @staticmethod
    def confirm_subscription(token):
        """Подтверждение подписки по токену"""
        try:
            subscriber = NewsSubscriber.objects.get(
                confirmation_token=token,
                confirmed=False,
                user__isnull=True  # Только для анонимных подписок
            )
            subscriber.confirmed = True
            subscriber.is_active = True
            subscriber.save()
            return subscriber
        except NewsSubscriber.DoesNotExist:
            return None

    @staticmethod
    def send_newsletter(news_item):
        """Отправка новости подписчикам"""
        subscribers = NewsSubscriber.objects.filter(
                is_active=True,
                news_type=news_item.type if news_item.type else None,
                confirmed=True
            ).exclude(
                models.Q(expires_at__lt=timezone.now()) | models.Q(user__isnull=False)
            )

        sent_count = 0
        for subscriber in subscribers:
            context = {
                'news_title': news_item.title,
                'news_content': news_item.main_text,
                'unsubscribe_url': (
                    f"https://ваш-сайт.ru/unsubscribe/"
                    f"?token={subscriber.confirmation_token}"
                )
            }

            subject = f"Новая новость: {news_item.title}"
            message = render_to_string('emails/newsletter.txt', context)
            html_message = render_to_string('emails/newsletter.html', context)

            try:
                send_mail(
                    subject,
                    message,
                    'news@ваш-сайт.ru',
                    [subscriber.user.email if subscriber.user else subscriber.email],
                    html_message=html_message
                )
                sent_count += 1
            except Exception as e:
                logger.error(f"Ошибка отправки новости {news_item.id} для {subscriber}: {e}")

        return sent_count

    @staticmethod
    def cleanup_expired_subscriptions():
        """Очистка просроченных подписок"""
        expired = NewsSubscriber.objects.filter(
            expires_at__lte=timezone.now(),
            user__isnull=True
        )
        count, _ = expired.delete()
        return count

    @staticmethod
    def unsubscribe(user=None, email=None, news_type_id=None):
        """Отписка пользователя или email"""
        if not user and not email:
            raise ValueError("Требуется email или пользователь")

        filters = {'user': user} if user else {'email': email}
        if news_type_id:
            filters['news_type_id'] = news_type_id

        deleted_count, _ = NewsSubscriber.objects.filter(**filters).delete()
        return deleted_count > 0

    @staticmethod
    def check_user_subscription(user, news_type_id=None):
        """Проверка наличия подписки у пользователя"""
        if not user.is_authenticated:
            return False

        return NewsSubscriber.objects.filter(
            user=user,
            news_type_id=news_type_id,
            is_active=True
        ).exists()