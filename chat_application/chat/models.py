from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.text import slugify


class RoomManager(models.Manager):

    def create_room(self, room_name, room_password):
        hashed_password = make_password(room_password)
        slug = slugify(room_name)
        room = self.create(room_name=room_name, slug=slug, room_password=hashed_password)
        return room


class RoomModel(models.Model):
    room_name = models.CharField(max_length=100, unique=True, null=False)
    slug = models.CharField(max_length=100, unique=True, null=False)
    room_password = models.CharField(max_length=100, null=False)
    objects = RoomManager()

    def __str__(self):
        return self.room_name


class MessageModel(models.Model):
    text = models.CharField(max_length=3000)
    user_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
