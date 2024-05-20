import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from rooms.views import room

from .models import Room, Message, Join
from django.contrib.auth.models import User

Join.objects.all().delete()

class ChatConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def save_member(self,user,room):
        Join.objects.create(room=room,user=user)
    
    @sync_to_async
    def remove_member(self,user):
        Join.objects.filter(user=user).delete()


    # @sync_to_async
    async def member_add(self):
        user = self.scope['user']
        room = await sync_to_async(Room.objects.get)(slug=self.room_name)
        await self.save_member(user,room)
    
    async def member_add(self):
        user = self.scope['user']
        room = await sync_to_async(Room.objects.get)(slug=self.room_name)
        await self.save_member(user,room)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'in_member',
                'newuser': user.username,
            }
        )

    async def member_left(self):
        user = self.scope['user']
        room = await sync_to_async(Room.objects.get)(slug=self.room_name)
        await self.remove_member(user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'out_member',
                'goneuser': user.username,
            }
        )


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print("\n"*4,self.scope,"\n"*4);
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.member_add()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.member_left()
    
    
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
    
    async def in_member(self, event):
        newuser = event['newuser']

        # Send message to WebSocket
        if newuser != self.scope['user'].username :
            await self.send(text_data=json.dumps({
                'newuser':newuser,
            }))

    async def out_member(self, event):
        goneuser = event['goneuser']

        # Send message to WebSocket
        if goneuser != self.scope['user'].username :
            await self.send(text_data=json.dumps({
                'goneuser':goneuser,
            }))

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
