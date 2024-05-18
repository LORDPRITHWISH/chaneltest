import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from rooms.views import room

from .models import Room, Message
from django.contrib.auth.models import User



class ChatConsumer(AsyncWebsocketConsumer):
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
    
    
    @sync_to_async
    def save_message(self,message,username,room):
        room = Room.objects.get(slug=room)
        user = User.objects.get(username=username)
        Message.objects.create(room=room,user=user,content=message)
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        # print(room,'room==========================================================================================================================')
        time = data['time']

        await self.save_message(message,username,room)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
                'time': time
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        time = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username':username,
            'room':room,
            'time':time
        }))
