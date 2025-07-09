from django.db import models
from main_app.models.base_user.user import BaseModel,User

class News(BaseModel):
    title = models.CharField(max_length=200)
    main_text = models.TextField()
    photo = models.ImageField(upload_to='news/photoes/')
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)

    def __str__(self):
        return f"{self.author.username or self.author.phone_number} — {self.text[:30]}"
        