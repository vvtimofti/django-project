from django.urls import path
from . import views


urlpatterns = [
    path("messages/<str:username>/", views.get_or_create_chatroom, name="start_chat"),
    path("messages/room/<room_name>/", views.chat_view, name="chat_room"),
]

