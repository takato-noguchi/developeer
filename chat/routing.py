from django.urls import path

from . import consumers

# Web Socketのルーティングを調整する
websocket_urlpatterns = [
    path( 'ws/{{room.id}}/', consumers.ChatConsumer),
]
