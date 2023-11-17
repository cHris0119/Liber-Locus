from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.contrib.auth.models import User
from .models import Auction, AuctionOffer, Book, Forum, Review, Notification
from django.utils import timezone

channel_layer = get_channel_layer()

@receiver(post_save, sender=Auction)
def auction_status_changed(sender, instance, **kwargs):
    group_name = f"auction_{instance.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "auction.status_changed",
            "message": {"status": instance.auction_state.name},
        },
    )

@receiver(post_save, sender=AuctionOffer)
def new_offer(sender, instance, **kwargs):
    group_name = f"auction_{instance.auction.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "auction.new_offer",
            "message": {"amount": instance.amount, "user": instance.user.username},
        },
    )


# Función para crear notificaciones
def create_notification(user, message):
    Notification.objects.create(
        message=message,
        created_at=timezone.now(),
        is_read=False,
        user=user,
    )



def send_notification_to_user(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user_id}",
        {
            'type': 'send_notification',
            'message': message,
        }
    )



@receiver(post_save, sender=Book)
def create_book_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Nuevo libro agregado: {instance.title}"
        Notification.objects.create(
            message=message,
            created_at=instance.created_at,  # Ajusta según el campo de fecha de tu modelo
            is_read=False,
            user=instance.seller,  # Ajusta según la relación del libro con el vendedor
        )
        # Enviar la notificación a través de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'message': message,
            }
        )

@receiver(post_save, sender=Forum)
def create_forum_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Nuevo foro creado: {instance.title}"
        Notification.objects.create(
            message=message,
            created_at=instance.created_at,  # Ajusta según el campo de fecha de tu modelo
            is_read=False,
            user=instance.author,  # Ajusta según la relación del foro con el autor
        )
        # Enviar la notificación a través de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'message': message,
            }
        )

@receiver(post_save, sender=Review)
def create_review_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Nueva reseña agregada para el libro {instance.book.title}"
        Notification.objects.create(
            message=message,
            created_at=instance.created_at,  # Ajusta según el campo de fecha de tu modelo
            is_read=False,
            user=instance.author,  # Ajusta según la relación de la reseña con el autor
        )
        # Enviar la notificación a través de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'message': message,
            }
        )

@receiver(post_save, sender=Book)
def update_book_notification(sender, instance, created, **kwargs):
    if not created:
        message = f"Libro actualizado: {instance.title}"
        Notification.objects.create(
            message=message,
            created_at=instance.updated_at,  # Ajusta según el campo de fecha de actualización de tu modelo
            is_read=False,
            user=instance.seller,
        )
        # Enviar la notificación a través de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'message': message,
            }
        )

@receiver(post_save, sender=Forum)
def update_forum_notification(sender, instance, created, **kwargs):
    if not created:
        message = f"Foro actualizado: {instance.title}"
        Notification.objects.create(
            message=message,
            created_at=instance.updated_at,  # Ajusta según el campo de fecha de actualización de tu modelo
            is_read=False,
            user=instance.author,
        )
        # Enviar la notificación a través de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'message': message,
            }
        )

@receiver(post_save, sender=Review)
def update_review_notification(sender, instance, created, **kwargs):
    if not created:
        message = f"Reseña actualizada para el libro {instance.book.title}"
        Notification.objects.create(
            message=message,
            created_at=instance.updated_at,  # Ajusta según el campo de fecha de actualización de tu modelo
            is_read=False,
            user=instance.author,
        )
        # Enviar la notificación a través de WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'message': message,
            }
        )