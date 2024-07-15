import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.chatroom = get_object_or_404(ChatRoom, room_name=self.room_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        message = RoomMessage.objects.create(
            room=self.chatroom,
            sender=self.user,
            body=body
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = RoomMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
            'chat_room': self.chatroom
        }
        html = render_to_string("chat/partials/chat_message.html", context=context)
        self.send(text_data=html)
    
    def message_delete(self, event):
        message = event["data"]
        context = {
            'message': message,
            'user': self.user,
            'chat_room': self.chatroom,
            'deletion': True
        }
        html = render_to_string("chat/partials/chat_message.html", context=context)
        self.send(text_data=html)
        