# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Notification

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        message = json.dumps({
            'type': 'notification',
            'message': 'Nueva notificación: {}'.format(instance.text),
        })
        async_to_sync(channel_layer.group_send)('notifications', {'type': 'send_notification', 'message': message})

