from django.urls import path
from .views import CreateRoomView, ChatRoomDetailView, MessageCreateView 

app_name = "chat"

urlpatterns = [
    path('', CreateRoomView.as_view(), name='room'),
    path('room/<uuid:pk>/', ChatRoomDetailView.as_view(), name='chat-room'),
    path('chat/', MessageCreateView.as_view(), name='chat'),
]