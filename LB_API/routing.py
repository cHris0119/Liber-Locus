from django.urls import path, re_path
from .consumer import LikesConsumer


ws_urlpatterns = [
    re_path(r'ws/consumer/likes/', LikesConsumer.as_asgi())
]