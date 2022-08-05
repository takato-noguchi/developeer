from audioop import reverse
from django.views.generic import CreateView, DetailView, ListView
from .models import ChatRoom, Message
from django.urls import reverse_lazy
from .forms import CreateRoomForm, MessageForm
from django.template import loader

# チャットルーム表示・作成機能
class CreateRoomView(CreateView):
    template_name = 'chat/index.html'
    model = ChatRoom
    form_class = CreateRoomForm
    success_url = reverse_lazy('projectlist')

    # チャットルームを5つ取得 -> 作成順に並び替え
    queryset = ChatRoom.objects.order_by('-created_at')[:5]

    def get_context_data(self):
        context = super().get_context_data()
        # 取得したquerysetをobjectsに代入
        context['objects'] = self.get_queryset()
        return context

    def get_success_url(self) -> str:
        return reverse('chat:chat-room', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super(CreateView, self).form_valid(form)

# 個別のチャットルーム表示機能
class ChatRoomDetailView(DetailView):
    template_name = 'chat/room.html'
    model = ChatRoom

    queryset = ChatRoom.objects\
        .prefetch_related('messages')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MessageForm'] = MessageForm(initial={'room': self.object})
        return context

# メッセージを作成
class MessageCreateView(CreateView):
    model = Message
    # メッセージは、チャットルームで
    template_name = 'chat/room.html'
    form_class = MessageForm
    success_url = reverse_lazy('projectlist')
    




