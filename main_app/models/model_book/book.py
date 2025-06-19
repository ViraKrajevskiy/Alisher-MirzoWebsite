from main_app.models.base_user.user import BaseModel,User
from django.db import models

class Book(BaseModel):
    title = models.CharField(max_length=70)
    AuthorName = models.CharField(max_length=60)
    date_made = models.DateField()
    description = models.TextField()
    photo = models.ImageField(upload_to='book/photos/', blank=True, null=True)
    file = models.FileField(upload_to='book/files/', blank=True, null=True)

class ComentBook(BaseModel):
    books = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='Book')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)

    def __str__(self):
        return f"{self.author.username or self.author.phone_number} — {self.text[:30]}"