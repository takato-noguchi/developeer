from django.contrib import admin
from .models import Room, Message, ChatRoom

admin.site.register(Room)
admin.site.register(ChatRoom)
admin.site.register(Message)