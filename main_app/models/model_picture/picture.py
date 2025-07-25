from django.db import models
from main_app.models.base_user.user import BaseModel,User

class Picture(BaseModel):
    title = models.CharField(max_length=40)
    style = models.CharField(max_length=60)
    date_made = models.DateTimeField()
    description_photo = models.TextField()
    picture = models.ImageField(upload_to='pictures/images/')

    def __str__(self):
        return self.title


    def like_count(self):
        return self.likes.count()

class CommentPicture(BaseModel):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='commentses')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)


    def like_count(self):
        return self.likes.count()


    def __str__(self):
        return f"{self.author.username or self.author.phone_number} — {self.text[:30]}"
        

class CommentPictureLike(models.Model):
    comment = models.ForeignKey(CommentPicture, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')  # 1 пользователь = 1 лайк на комментарий

    def __str__(self):
        return f"{self.user.username} liked comment {self.comment.id}"

class PictureLike(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('picture', 'user')  # Один пользователь — один лайк

    def __str__(self):
        return f"{self.user.username} liked picture {self.picture.title}"
