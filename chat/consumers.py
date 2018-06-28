from channels.generic.websocket import AsyncWebsocketConsumer
import json


from django.utils import timezone
from channels.db import database_sync_to_async

from chat.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_{}'.format(self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        self.user_id = self.scope['user'].id
        self.room_id = await self.get_room_id()
        self.user_name = self.scope['user'].username
        self.avatar_url = self.scope['user'].avatar.url

    @database_sync_to_async
    def get_room_id(self):
        return Room.objects.get(name=self.room_name).id

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        date = timezone.now()

        await self.save_message_to_db(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': self.user_name,
                'date': date.isoformat(),
                'avatar_url': self.avatar_url,
            }
        )


    @database_sync_to_async
    def save_message_to_db(self, message):
        return Message.objects.create(
            text=message,
            author_id=self.user_id,
            room_id=self.room_id,
        ).save()


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        date = event['date']
        avatar_url = event['avatar_url']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'date': date,
            'avatar_url': avatar_url,
        }))