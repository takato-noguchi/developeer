from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
from re import template
from typing import List
from django.views.generic import CreateView, DetailView, ListView
from .models import ChatRoom, Message
from django.urls import reverse_lazy
from .forms import CreateRoomForm, MessageForm
from django.template import loader

# ルーム作成ページ
def index(request):
    room_list = ChatRoom.objects.order_by('-created_at')[:5]
    template = loader.get_template('chat/index.html')
    context = {
        'room_list': room_list,
    }
    return (template.render(context, request))

# チャット作成
def chat(request, room_name):
    messages = Message.objects.filter(room__name=room_name).order_by('-created_at')[:50]
    room = ChatRoom.objects.filter(name=room_name)[0]
    template = loader.get_template('chat/chat_room.html')
    context = {
        'messages': messages,
        'room': room
    }
    return HttpResponse(template.render(context, request))

# ルーム作成
def room(request):
    name = request.POST.get("room_name")
    room = ChatRoom.objects.create(name=name)
    return HttpResponseRedirect(reverse('chat:chat_room', args=[name]))

# ルームの詳細ページ
class RoomDetailView(DetailView):
    # 表示するルーム
    model = Message
    template_name = 'chat/room.html'

# メッセージを作成
class MessageCreateView(CreateView):
    model = Message
    # メッセージは、チャットルームで
    template_name = 'chat/room.html'
    form_class = MessageForm




