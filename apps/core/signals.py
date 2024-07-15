from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from apps.posts.models import Post, Notification
from apps.chat.models import RoomMessage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Post)
def send_notification_on_reply(sender, instance, created, **kwargs):
    if created:
        if not instance.parent_post or instance.parent_post.user == instance.user:
            return
        
        Notification.objects.create(
            receiver=instance.parent_post.user,
            post_creator=instance,
        )
        channel_layer = get_channel_layer()
        group_name = "user-notifications"
        event = {
            "type": "user_reply",
            "data": instance
        }
        async_to_sync(channel_layer.group_send)(group_name, event)


@receiver(post_save, sender=Post)
def send_notification_on_feed_update(sender, instance, created, **kwargs):
    if created:
        if instance.parent_post:
            return
        channel_layer = get_channel_layer()
        group_name = "user-notifications"
        event = {
            "type": "feed_update",
            "data": instance
        }
        async_to_sync(channel_layer.group_send)(group_name, event)


@receiver(post_delete, sender=RoomMessage)
def send_message_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    room_group_name = f"chat_{instance.room.room_name}"
    event = {
        "type": "message_delete",
        "data": instance
    }
    async_to_sync(channel_layer.group_send)(room_group_name, event)
