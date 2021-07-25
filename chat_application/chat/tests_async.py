from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.urls import re_path
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from .consumers import ChatConsumer
from .models import RoomModel


class ChatTest(TransactionTestCase):

    @sync_to_async
    def set_data(self):
        room = RoomModel.objects.create_room('Room1', 'room_password_123')
        room_slug = room.slug
        user1 = User.objects.create_user(username='User1', password='user_password_123')
        user2 = User.objects.create_user(username='User2', password='user_password_456')
        return room_slug, user1, user2

    async def test_one_user(self):
        application = URLRouter([
            re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
        ])
        room_slug, user, _ = await self.set_data()
        communicator = WebsocketCommunicator(application, f'/ws/chat/{room_slug}/')
        communicator.scope['user'] = user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.send_json_to({'message': 'hello'})
        response = await communicator.receive_json_from()
        self.assertEqual('hello', response['message'])
        await communicator.disconnect()

    async def test_between_two_users(self):
        application = URLRouter([
            re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
        ])
        room_slug, user1, user2 = await self.set_data()
        communicator1 = WebsocketCommunicator(application, f'/ws/chat/{room_slug}/')
        communicator1.scope['user'] = user1
        connected, _ = await communicator1.connect()
        self.assertTrue(connected)
        communicator2 = WebsocketCommunicator(application, f'/ws/chat/{room_slug}/')
        communicator2.scope['user'] = user2
        connected, _ = await communicator2.connect()
        self.assertTrue(connected)
        await communicator1.send_json_to({'message': 'hello'})
        response = await communicator2.receive_json_from()
        self.assertEqual('hello', response['message'])
        self.assertEqual(user1.username, response['user'])
        await communicator1.disconnect()
        await communicator2.disconnect()
