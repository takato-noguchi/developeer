from re import template
from django.views.generic import CreateView
from .models import ChatRoom, Message
from django.urls import reverse_lazy
from .forms import CreateRoomForm, MessageForm

# ルームを作成
class ChatRoomView(CreateView):
    model = ChatRoom
    # ルーム作成はプロジェクトに紐づける
    template_name = 'projects/projectDetail.html'
    form_class = CreateRoomForm

# メッセージを作成
class ChatView(CreateView):
    model = Message
    # メッセージは、チャットルームで
    template_name = 'chat/room.html'
    form_class = MessageForm




