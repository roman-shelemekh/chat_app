import json
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RoomModel


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'user_connection', 'event': 'connect', 'user': self.scope['user'].username}
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'user_connection', 'event': 'disconnect', 'user': self.scope['user'].username}
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        self.message = json.loads(text_data).get('message')
        data = {'type': 'chat_message'}
        data.update(await self.create_message())
        await self.channel_layer.group_send(self.room_group_name, data)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'timestamp': event['timestamp']
        }))

    async def user_connection(self, event):
        await self.send(text_data=json.dumps({
            'event': event['event'],
            'user': event['user'],
        }))

    @database_sync_to_async
    def create_message(self):
        room = RoomModel.objects.get(slug=self.room_name)
        user = User.objects.get(username=self.scope['user'])
        msg = room.messagemodel_set.create(text=self.message, user=user)
        return {
            'message': msg.text,
            'user': self.scope['user'].username,
            'timestamp': msg.timestamp.strftime("%d/%m/%Y, %H:%M")
        }


