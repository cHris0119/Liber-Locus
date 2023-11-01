from django.urls import re_path
from .consumer import LikesConsumer, SubastaConsumer


ws_urlpatterns = [
    re_path(r'ws/subasta/(?P<subasta_id>\d+)/$', SubastaConsumer.as_asgi()),
    re_path(r'ws/consumer/likes/', LikesConsumer.as_asgi())
]