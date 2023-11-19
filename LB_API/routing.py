from django.urls import re_path
from .consumer import LikesConsumer, AuctionConsumer, Chat_Room, NotificationConsumer
from .consumer import NotificationConsumer
from .signals import send_notification
from django.db.models.signals import post_save
from.models import Notification


ws_urlpatterns = [
    re_path(r'ws/auction/(?P<auction_id>\d+)/$', AuctionConsumer.as_asgi()),
    re_path(r'ws/consumer/likes/', LikesConsumer.as_asgi()),
    re_path(r'ws/notifications/', NotificationConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<chatroom_id>\d+)/$', Chat_Room.as_asgi()),
    re_path(r'ws/notifications/', NotificationConsumer.as_asgi())
    
]

post_save.connect(send_notification, sender=Notification)
