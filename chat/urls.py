from django.urls import path
from .views import CreateRoomView, ChatView

app_name = "chat"

urlpatterns = [
    path('', CreateRoomView, name='chat' ),
    path('room/<int:pk>', ChatView.as_view(), name='room')
]