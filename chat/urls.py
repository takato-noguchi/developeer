from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.chat, name='chat' ),
    path('room/<uuid:room_id>', views.room, name='room')
]