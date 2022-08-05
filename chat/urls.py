from django.urls import path
from .views import CreateRoomView, ChatRoomDetailView, MessageCreateView 

app_name = "chat"

urlpatterns = [
    path('', CreateRoomView.as_view(), name='room'),
    path('room/<int:pk>/', ChatRoomDetailView.as_view(), name='chat-room'),
    path('room/', MessageCreateView.as_view(), name='chat'),
]