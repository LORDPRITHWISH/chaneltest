from django.urls import path
from fastapi import WebSocket
from . import consumers

WebSocket.url_pattern = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]