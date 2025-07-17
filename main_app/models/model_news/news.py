from django.db import models
from main_app.models.base_user.user import BaseModel,User


class NewsType(BaseModel):
    type_news = [
        ('general','General'),
        ('pictures','Pictures'),
        ('albums','Albums'),
        ('books','Books')
    ]
    name = models.CharField(max_length=20, choices=type_news, unique=True)


class News(BaseModel):
    title = models.CharField(max_length=200)
    main_text = models.TextField()
    photo = models.ImageField(upload_to='news/photoes/')
    published_at = models.DateTimeField(auto_now_add=True)

    type = models.ForeignKey(NewsType, on_delete=models.SET_NULL, null=True, related_name='news')


    def __str__(self):
        return self.title


class Comment(BaseModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username or self.author.phone_number} — {self.text[:30]}"

    def like_count(self):
        return self.likes.count()

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')  # Один пользователь — один лайк на комментарий

    def __str__(self):
        return f"{self.user} liked comment {self.comment.id}"
        