from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from main_app.models.model_news.news import NewsSubscriber

def subscribe_to_news(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        website = request.POST.get('website')  # honeypot

        if website:  # бот
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if request.user.is_authenticated:
            obj, created = NewsSubscriber.objects.get_or_create(user=request.user)
            if created:
                messages.success(request, "Вы подписались на новости!")
                send_mail(
                    subject='Подписка на новости',
                    message='Спасибо за подписку, вы будете получать новости сайта.',
                    from_email='no-reply@твойдомен.uz',
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )
            else:
                messages.info(request, "Вы уже подписаны.")
        else:
            if email and not NewsSubscriber.objects.filter(email=email).exists():
                NewsSubscriber.objects.create(email=email)
                messages.success(request, "Вы подписались на новости!")
                send_mail(
                    subject='Подписка на новости',
                    message='Спасибо за подписку, вы будете получать новости сайта.',
                    from_email='no-reply@твойдомен.uz',
                    recipient_list=[email],
                    fail_silently=False,
                )
            else:
                messages.info(request, "Этот email уже подписан.")

    return redirect(request.META.get('HTTP_REFERER', '/'))
    