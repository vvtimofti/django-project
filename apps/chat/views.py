from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.db.models import Count
from .forms import RoomMessageForm

from .models import ChatRoom, RoomMessage


User = get_user_model()

@login_required
def chat_view(request, room_name):
    chat_room = get_object_or_404(ChatRoom, room_name=room_name)
    room_messages = chat_room.chat_messages.all()
    form = RoomMessageForm()
    chatrooms = request.user.chat_rooms.annotate(
        message_count=Count('chat_messages')
    ).filter(message_count__gte=1)

    chat_partners = User.objects.exclude(
        id=request.user.id).filter(chat_rooms__in=chatrooms)

    other_user = None
    if chat_room.is_private:
        if request.user not in chat_room.members.all():
            raise Http404()
        for member in chat_room.members.all():
            if member != request.user:
                other_user = member
                break

    if request.method == "DELETE":
        RoomMessage.objects.filter(id=request.body.decode("utf-8").split("=")[-1]).delete()
        return HttpResponse(status=200)
    
    context = {
        "room_messages": room_messages,
        "other_user": other_user,
        "room_name": room_name,
        "form": form,
        "room": chat_room,
        "chatrooms": chatrooms,
        "members": chat_partners,
    }

    return render(request, "chat/chat.html", context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect("messages")

    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_rooms.filter(is_private=True)

    existing_chatroom = my_chatrooms.filter(members=other_user).first()
    if existing_chatroom:
        return redirect("chat_room", room_name=existing_chatroom.room_name)

    room = ChatRoom.objects.create(is_private=True)
    room.members.add(request.user, other_user)

    return redirect("chat_room", room_name=room.room_name)
