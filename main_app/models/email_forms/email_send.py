from django.db import models
from django.contrib.auth import get_user_model
from main_app.models.base_user.user import BaseModel


User = get_user_model()

class ContactMessage(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
