from email.policy import default
from django.db import models
from app.models import Plan
from django.conf import settings
import uuid
from django.utils import timezone

class ChatRoom(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.OneToOneField(
        Plan, on_delete=models.CASCADE,
        default=''
    )
    created_at = models.DateTimeField(default=timezone.now)

class Message(models.Model):
    message = models.CharField(max_length=100)
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE,
        related_name='messages'
    )
    userMessage = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name= 'message',
        on_delete= models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
