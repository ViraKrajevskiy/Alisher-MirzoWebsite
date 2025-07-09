from main_app.models.base_user.user import BaseModel,User
from django.db import models

class Album(BaseModel):
    title = models.CharField(max_length=70)
    AuthorName = models.CharField(max_length=60)
    date_made = models.DateField()
    descriptionalbum = models.TextField()
    photoalbum = models.ImageField(upload_to='book/albumphoto/', blank=True, null=True)
    filealbum = models.FileField(upload_to='book/filealbum/', blank=True, null=True)

class ComentAlbum(BaseModel):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='albums')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)

    def __str__(self):
        return f"{self.author.username or self.author.phone_number} — {self.text[:30]}"