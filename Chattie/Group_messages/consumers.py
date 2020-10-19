import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Group, GroupMessage
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room_id = text_data_json['roomName']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room_id': room_id
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        room_id = event['room_id']
        user = User.objects.get(username=username)
        group = Group.objects.get(pk=room_id)
        new_message = GroupMessage(text=message, group=group, user=user)
        new_message.save()

        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
