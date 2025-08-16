import random
import logging
from django.utils.timezone import now
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

logger = logging.getLogger(__name__)  # Для логирования ошибок

def generate_code():
    return f"{random.randint(100000, 999999)}"

def send_confirmation_code(user):
    code = generate_code()
    user.confirmation_code = code
    user.code_created_at = now()
    user.save()

    subject = 'Сброс пароля'
    message = f"Ваш одноразовый код для сброса пароля: {code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except BadHeaderError:
        logger.error("Ошибка заголовка при отправке email.")
    except Exception as e:
        logger.error(f"Ошибка при отправке email пользователю {user.email}: {str(e)}")
        