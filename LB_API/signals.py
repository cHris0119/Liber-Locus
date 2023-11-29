# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Notification, PurchaseDetail, AuctionOffer
from .functions import int_id
from django.utils import timezone

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        message = json.dumps({
            'type': 'send_notification',
            'id': instance.id,
            'message': f'Nueva notificación: {instance.message}',
            'created_at': instance.created_at.strftime("%Y-%m-%d"), 
            'is_read': instance.is_read,
            'user': instance.user.id      
        })
        async_to_sync(channel_layer.group_send)(f'notifications_{instance.user.id}', 
                                                {'type': 'send_notification', 
                                                 'id': instance.id,
                                                 'message': message,
                                                 'created_at': instance.created_at.strftime("%Y-%m-%d"),
                                                 'is_read': instance.is_read,
                                                 'user':instance.user.id})


