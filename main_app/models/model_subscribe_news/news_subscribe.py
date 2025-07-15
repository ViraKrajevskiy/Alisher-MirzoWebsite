from django.db import models
from main_app.models.base_user.user import BaseModel,User

class NewsSubscriber(BaseModel):
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
