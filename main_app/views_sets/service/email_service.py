from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from main_app.models.model_news.news import News, NewsSubscriber

def prepare_email_content(news, subscriber):
    context = {
        'news': news,
        'subscriber': subscriber,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}news/unsubscribe/{subscriber.id}/"
    }

    text_content = f"{news.title}\n\n{news.main_text}"
    html_content = render_to_string('emails/newsletter.html', context)

    return {
        'subject': f"{news.type.get_name_display()}: {news.title}",
        'text_content': text_content,
        'html_content': html_content
    }

def send_single_email(email_data, to_email):
    msg = EmailMultiAlternatives(
        email_data['subject'],
        email_data['text_content'],
        settings.DEFAULT_FROM_EMAIL,
        [to_email]
    )
    msg.attach_alternative(email_data['html_content'], "text/html")
    msg.send()