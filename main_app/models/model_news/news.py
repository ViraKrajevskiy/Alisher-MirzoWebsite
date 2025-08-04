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

class NewsSubscriber(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='news_subscriptions')
    email = models.EmailField(null=True, blank=True, unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_news_user_sub')  # если user
        ]

    def __str__(self):
        return self.user.email if self.user else self.email

