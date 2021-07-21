import json
from django.contrib.auth.models import User
from channels.generic.websocket import WebsocketConsumer
from .models import MessageModel, RoomModel


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        room = RoomModel.objects.get(slug=text_data_json.get('room_slug'))
        user = User.objects.get(username=text_data_json.get('user'))
        msg = room.messagemodel_set.create(text=text_data_json.get('message'), user_name=user)
        self.send(text_data=json.dumps({
            'message': msg.text,
            'user': msg.user_name.username,
            'timestamp': msg.timestamp.strftime("%d/%m/%Y, %H:%M")
        }))