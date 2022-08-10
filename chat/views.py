from audioop import reverse
from django.views.generic import CreateView, DetailView
from .models import ChatRoom, Message, Plan
from django.urls import reverse_lazy
from .forms import CreateRoomForm, MessageForm
from django.template import loader
from django.contrib import messages
from django.shortcuts import render, redirect

# チャットルーム表示・作成機能
class CreateRoomView(CreateView):
    template_name = 'projects/projectDetail.html'
    model = ChatRoom
    form_class = CreateRoomForm
    success_url = reverse_lazy('projectlist')

    # どのプロジェクトに送るか
    def room_create(request):
        plan_id = request.POST.get("plan")
        data = {"plan": plan_id}
        form = CreateRoomForm(data=data)

        if form.is_valid():
            form.save()
        else:
            messages.error(request, "コメントが投稿できませんでした")

        return redirect("projectlist")

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

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.POST.dict()
        data['userMessage'] = user.id
        form = MessageForm(data=data)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    




