from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Auction, AuctionOffer

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