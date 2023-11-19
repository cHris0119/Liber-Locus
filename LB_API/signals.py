# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Notification, PurchaseDetail, AuctionOffer
from django.utils import timezone

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        message = json.dumps({
            'type': 'notification',
            'message': 'Nueva notificación: {}'.format(instance.text),
        })
        async_to_sync(channel_layer.group_send)('notifications', {'type': 'send_notification', 'message': message})

@receiver(post_save, sender=PurchaseDetail)
def notify_seller_book_purchased(sender, instance, created, **kwargs):
    if created and instance.book.seller:
        message = f"Tu libro '{instance.book.title}' ha sido comprado en el marketplace."
        Notification.objects.create(
            message=message,
            created_at=timezone.now(),
            is_read=False,
            user=instance.book.seller,
            related_book=instance.book,
            related_purchase=instance,
        )
        # Envío a través de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.book.seller.id}",
            {
                'type': 'send_notification',
                'message': message,
            }
        )

@receiver(post_save, sender=AuctionOffer)
def notify_auction_winner(sender, instance, created, **kwargs):
    if created:
        auction = instance.auction
        # Obtener la oferta máxima actual para la subasta
        winning_offer = AuctionOffer.objects.filter(auction=auction).order_by('-amount').first()
        if winning_offer and instance == winning_offer:
            winner = instance.user
            # Crear la notificación para el ganador de la subasta
            message = f"¡Felicidades! Has ganado la subasta del libro {auction.book.title}. Por favor, procede con el pago."
            Notification.objects.create(
                message=message,
                created_at=timezone.now(),
                is_read=False,
                user=winner,
                related_auction=auction,
            )
            # Envío a través de WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"notifications_{winner.id}",
                {
                    'type': 'send_notification',
                    'message': message,
                }
            )