from django.urls import re_path
from .consumer import LikesConsumer, AuctionConsumer


ws_urlpatterns = [
    re_path(r'ws/auction/(?P<auction_id>\d+)/$', AuctionConsumer.as_asgi()),
    re_path(r'ws/consumer/likes/', LikesConsumer.as_asgi())
]