# chat/consumers.py
import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, Room
from channels.db import database_sync_to_async


class ChatRoomConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def saveMessage(self, message):
        room = Room.objects.get(pk=self.room_id)

        Message.objects.create(
            user=self.scope['user'],
            room=room,
            body=message
        )

        room.participants.add(self.scope['user'])

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "chat_%s" % self.room_id

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.saveMessage(message=message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.scope['user'].username
            })

    async def chat_message(self, event):
        message = event["message"]
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))
