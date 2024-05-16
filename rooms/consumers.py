import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# from .models import Room, Message
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from django.utils import timezone
# from django.core import serializers


class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        