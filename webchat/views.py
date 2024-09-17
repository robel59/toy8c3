from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, ChatUser, Message

@login_required
def home(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        # Create or get the user
        user, created = ChatUser.objects.get_or_create(email=email, defaults={
            'name': user_name,
            'phone_number': phone_number
        })

        # Create or get the room
        room, created = Room.objects.get_or_create(email = email, user=user)

        # Redirect to the chat room
        return redirect('webchat:chat_room', email=user.email)

    return render(request, 'webchat/register.html')

@login_required
def chat_room(request, email):
    user = ChatUser.objects.get(email=email)
    room = user.rooms.first()  # Assuming one room per user
    messages = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'webchat/chat.html', {
        'room': room,
        'user': user,
        'messages': messages
    })

@login_required
def team_dashboard(request):
    rooms = Room.objects.all().select_related('user')
    return render(request, 'webchat/team_dashboard.html', {
        'rooms': rooms
    })

@login_required
def team_chat_room(request, email):
    user = ChatUser.objects.get(email=email)
    room = user.rooms.first()  # Assuming one room per user
    messages = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'webchat/team_chat_room.html', {
        'room': room,
        'user': user,
        'messages': messages
    })
