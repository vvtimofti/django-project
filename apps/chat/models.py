from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import shortuuid

User = get_user_model()


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=150, unique=True, default=shortuuid.uuid)
    members = models.ManyToManyField(User, related_name="chat_rooms", blank=True)
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.room_name
    

class RoomMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name="chat_messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.body}"

    class Meta:
        ordering = ["-created"]


class MessageNotification(models.Model):
    room = models.ForeignKey(ChatRoom, related_name="room_notifications", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
