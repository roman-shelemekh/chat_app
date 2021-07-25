from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse
from .models import RoomModel


@tag('chat_sync')
class IndexViewTest(TestCase):

    def setUp(self):
        self.url = reverse('chat:index')
        self.room = RoomModel.objects.create_room('Room1', 'some_password_123')
        self.user = User.objects.create_user(username='User1', password='user_password_123')

    def test_enter_room_not_authenticated(self):
        data = {'room_name': 'Room1', 'room_password': 'some_password_123', 'button': 'enter'}
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response=response, expected_url=reverse('chat:login') + '?next=/chat/room1/')

    def test_enter_room_authenticated(self):
        data = {'room_name': 'Room1', 'room_password': 'some_password_123', 'button': 'enter'}
        self.client.login(username='User1', password='user_password_123')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response=response, expected_url=reverse('chat:room', args=['room1']))

    def test_enter_room_wrong_password(self):
        data = {'room_name': 'Room1', 'room_password': 'some_password_456', 'button': 'enter'}
        response = self.client.post(self.url, data)
        self.assertFormError(
            response=response,
            form='enter_form',
            field=None,
            errors='Неверный пароль.'
        )

    def test_enter_room_not_existing(self):
        data = {'room_name': 'Room2', 'room_password': 'some_password_456', 'button': 'enter'}
        response = self.client.post(self.url, data)
        self.assertFormError(
            response=response,
            form='enter_form',
            field=None,
            errors='Комнаты c таким названием не существует.'
        )

    def test_create_room_same_name(self):
        data = {
            'room_name': 'Room1',
            'room_password1': 'some_password_456',
            'room_password2': 'some_password_456',
            'button': 'create'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response=response,
            form='create_form',
            field='room_name',
            errors='Комната с таким названием уже существует.'
        )

    def test_create_new_room_not_authenticated(self):
        data = {
            'room_name': 'Room2',
            'room_password1': 'some_password_456',
            'room_password2': 'some_password_456',
            'button': 'create'
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response=response, expected_url=reverse('chat:login') + '?next=/chat/room2/')
        self.assertQuerysetEqual(RoomModel.objects.all(), ['Room1', 'Room2'], ordered=False, transform=str)

    def test_create_new_room_authenticated(self):
        data = {
            'room_name': 'Room2',
            'room_password1': 'some_password_456',
            'room_password2': 'some_password_456',
            'button': 'create'
        }
        self.client.login(username='User1', password='user_password_123')
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response=response, expected_url=reverse('chat:room', args=['room2']))
        self.assertQuerysetEqual(RoomModel.objects.all(), ['Room1', 'Room2'], ordered=False, transform=str)
