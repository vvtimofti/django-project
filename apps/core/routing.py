from django.urls import path
from .consumers import NotificationConsumer
from apps.chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    path("ws/chatroom/<room_name>/", ChatConsumer.as_asgi())
]