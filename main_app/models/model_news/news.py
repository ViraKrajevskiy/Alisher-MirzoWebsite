from django.db import models
from main_app.models.base_user.user import BaseModel, User

class NewsTypeChoices(models.TextChoices):
    GENERAL = 'general', 'General'
    PICTURES = 'pictures', 'Pictures'
    ALBUMS = 'albums', 'Albums'
    BOOKS = 'books', 'Books'


class NewsType(BaseModel):
    name = models.CharField(max_length=20, choices=NewsTypeChoices.choices, unique=True)

    def __str__(self):
        return self.get_name_display()


class News(BaseModel):
    title = models.CharField(max_length=200)
    main_text = models.TextField()
    photo = models.ImageField(upload_to='news/photos/')
    published_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(NewsType, on_delete=models.SET_NULL, null=True, related_name='news')

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-published_at']


class Comment(BaseModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)

    def __str__(self):
        return f"{self.author.username} — {self.text[:30]}"

    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']


class CommentLikes(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f"{self.user.username} liked comment {self.comment.id}"


class NewsLike(BaseModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('news', 'user')

    def __str__(self):
        return f"{self.user.username} liked news '{self.news.title}'"

from django.core.validators import EmailValidator
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone

class NewsSubscriber(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subscriptions'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        validators=[EmailValidator(message="Введите корректный email")]
    )
    news_type = models.ForeignKey(
        NewsType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Тип новостей"
    )
    is_active = models.BooleanField(default=True)
    confirmation_token = models.CharField(max_length=64, blank=True)
    confirmed = models.BooleanField(default=False)
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Истекает (для анонимов)"
    )

    class Meta:
        constraints = [
            # Постоянная подписка для пользователей
            models.UniqueConstraint(
                fields=['user', 'news_type'],
                name='unique_user_subscription',
                condition=models.Q(user__isnull=False)
            ),
            # Временная подписка для email
            models.UniqueConstraint(
                fields=['email', 'news_type'],
                name='unique_email_subscription',
                condition=models.Q(email__isnull=False)
            ),
            # Обязательно user ИЛИ email
            models.CheckConstraint(
                check=(models.Q(user__isnull=False) | models.Q(email__isnull=False)),
                name='require_user_or_email'
            )
        ]
        verbose_name = "Подписчик новостей"
        verbose_name_plural = "Подписчики новостей"

    def save(self, *args, **kwargs):
        # Генерация токена для анонимов
        if not self.confirmation_token and self.email:
            self.confirmation_token = get_random_string(64)

        # Установка срока действия для анонимов
        if self.email and not self.user and not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=10)

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return bool(
            self.expires_at and
            timezone.now() > self.expires_at
        )

    def __str__(self):
        identifier = self.user.username if self.user else self.email
        news_type = self.news_type.name if self.news_type else "все типы"
        status = "активна" if self.is_active and not self.is_expired else "неактивна"
        return f"{identifier} → {news_type} ({status})"