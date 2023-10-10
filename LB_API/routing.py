from django.urls import path
from .consumer import LikesConsumer


ws_urlpatterns = [
    path('ws/consumer/likes', LikesConsumer.as_asgi())
]