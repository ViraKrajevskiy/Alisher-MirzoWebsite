import random
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

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

    send_mail(subject, message, from_email, recipient_list)
    