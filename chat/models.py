from django.db import models
from app.models import User, Plan
from django.conf import settings
import uuid

class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userRoom = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name= 'room',
        on_delete= models.CASCADE
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE
    )

class Message(models.Model):
    message = models.CharField(max_length=100)
    room = models.ForeignKey(
        Plan, on_delete=models.CASCADE
    )
    userMessage = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name= 'message',
        on_delete= models.CASCADE
    )
    created_at = models.DateField(auto_now_add=True)
