from django.db import models
from apps.application.models import User
from datetime import datetime
# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages")
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    message = models.ForeignKey(Message, related_name="comments")
    user = models.ForeignKey(User, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
