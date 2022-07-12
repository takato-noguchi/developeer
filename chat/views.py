from django.shortcuts import render

def chat( request ):
    return render( request, 'chat.html')

def room(request):
    return render(request, 'room.html')