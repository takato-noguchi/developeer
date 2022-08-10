from dataclasses import field
from django import forms
from .models import ChatRoom, Message

# ルーム作成フォーム
class CreateRoomForm(forms.ModelForm):

    class Meta:
        model = ChatRoom
        fields = ['plan',]

        widgets = {
            'plan': forms.HiddenInput(),
        }

# メッセージ作成フォーム
class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['message', 'room', 'userMessage',]

        widgets = {
            'room': forms.HiddenInput(),
            'userMessage': forms.HiddenInput(),
        }

        labels = {
            'message': "",
        }
