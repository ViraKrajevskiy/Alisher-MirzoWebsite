from django.db import models
from main_app.models.base_user.user import BaseModel,User

class Picture(BaseModel):
    title = models.CharField(max_length=40)
    date_made = models.DateTimeField()
    description_photo = models.TextField()
    picture = models.ImageField(upload_to='pictures/images/')

class CommentPicture(BaseModel):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='imges')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)

    def __str__(self):
        return f"{self.author.username or self.author.phone_number} — {self.text[:30]}"