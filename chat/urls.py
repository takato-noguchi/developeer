from django.urls import path
from .views import index, chat, room

app_name = "chat"

urlpatterns = [
    path('', index, name='room'),
    path('room/<str:room_name>/', chat, name='chat-room'),
    path('room/', room, name='chat'),
]