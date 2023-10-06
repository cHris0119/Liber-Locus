from django.urls import path
from .consumer import WSConsumer


ws_urlpatterns = [
    path('ws/consumer/likes', WSConsumer.as_asgi())
]