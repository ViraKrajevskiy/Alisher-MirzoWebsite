from main_app.models.base_user.user import BaseModel, User
from django.db import models

class Book(BaseModel):
    title = models.CharField(max_length=70)
    AuthorName = models.CharField(max_length=60)
    date_made = models.DateField()
    description = models.TextField()
    photo = models.ImageField(upload_to='book/photos/', blank=True, null=True)
    file = models.FileField(upload_to='book/files/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} — {self.AuthorName}"

    def like_count(self):
        return self.likes.count()  # теперь это будет работать

class BookLike(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} liked book {self.book.title}"

class ComentBook(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)

    def __str__(self):
        return f"{self.author.username} — {self.text[:30]}"

class CommentBookLike(models.Model):
    comment = models.ForeignKey(ComentBook, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f"{self.user.username} liked comment {self.comment.id}"


