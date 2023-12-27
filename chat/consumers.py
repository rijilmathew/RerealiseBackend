import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Room
from channels.auth import UserLazyObject
from authentification.models import User
from .serializers import MessageSerializer




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('self.scope:', self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print('self.room_name:', self.room_name)
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        # Accept the WebSocket connection
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data.get('sender')  # Extract sender information

        print('WebSocket message data:', data)
        print()

        if sender:
            user = await database_sync_to_async(User.objects.get)(id=sender)
            self.scope['user'] = user

        # Create and save the message
        new_message = await self.create_message(message)
        print('newmessage',new_message)

        # Broadcast the message to all members of the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': new_message,
            },
        )


    async def create_message(self, message):
        room = await database_sync_to_async(self.get_room)(self.room_name)
        user = self.scope['user']
        print('create user', user)

        # Use database_sync_to_async for the database operation
        new_message = await database_sync_to_async(Message.objects.create)(
            user=user,
            content=message,
            room=room,
        )

        # Convert the message content to JSON format
        json_message = {
            'content': new_message.content,
            'timestamp': new_message.timestamp.isoformat(),
            'user': new_message.user.id,
        }

        return json_message

    def get_room(self, room_name):
        print('room name:',room_name)
        return Room.objects.get(name=room_name)




    async def save_message(self, new_message):
        new_message.save()

    async def chat_message(self, event):
        message = event['message']
        print('chat message ',message)
       

        # Broadcast the message to all members of the room
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'message': message,
        })
        )

        