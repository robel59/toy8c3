import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatUser, Message, Room, SystemResponse
from asgiref.sync import sync_to_async
import re


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.email = self.scope['url_route']['kwargs']['email']
        #self.room_group_name = f'chat_{self.email}'
        self.room_group_name = self.sanitize_group_name(f"chat_{self.email}")


        self.room = await self.get_room(self.email)
        self.user = await self.get_user(self.email)
        self.name = await self.get_user1(self.email)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send_all_message()


    async def disconnect(self, close_code):

        await self.room_off(self.email)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_all_message(self):
        messages = await self.get_sorted_message()

        room_data = []
        for message in messages:

            room_data.append({
                'message': message.content,
                'sender': self.email,
                'user':self.name,
                'type1': 'client' if message.is_user else "other",

            })

        await self.send(text_data=json.dumps({
            'type': 'all_message',
            'messages': room_data,
        }))


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']  # 'client' or 'team'
        try:
            type = text_data_json['type']  # 'client' or 'team'
        except:
            type = 'other'

        print("kkkkkkk")
        print(text_data_json)

        # Save the message
        await self.save_message(self.room, self.user, message, sender, type)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'user':self.name,
                'type1':type
            }
        )

        if sender == 'client':
            # Generate a response from the system user if it's a client message
            system_response = await self.generate_system_response(message)

            if system_response:
                system_user = await self.get_system_user()
                await self.save_message(self.room, system_user, system_response, 'system', 'system')

                # Send system user's message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': system_response,
                        'user':'system',
                        'sender': 'system',
                        'type1':'system'
                    }
                )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        type = event['type1']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': "message",
            'message': message,
            'sender': sender,
            'user': self.name,
            'type1':type
        }))

    @sync_to_async
    def get_sorted_message(self):
        return list(Message.objects.filter(room = self.room))

    @sync_to_async
    def get_room(self, email):
        user = ChatUser.objects.get(email=email)
        room = user.rooms.first()
        room.set_online_state(True)
        return room

    @sync_to_async
    def room_off(self, email):
        try:
            room = Room.objects.get(email=email)
            room.set_online_state(False)
        except Room.DoesNotExist:
            pass

    @sync_to_async
    def get_user(self, email):
        return ChatUser.objects.get(email=email)
    
    @sync_to_async
    def get_user1(self, email):
        return ChatUser.objects.get(email=email).name

    @sync_to_async
    def save_message(self, room, user, message, sender, type):
        if type == 'client':
            Message.objects.create(room=room, user=user, content=message)
        else:
            Message.objects.create(room=room, user=user, content=message, is_user = False)


    @sync_to_async
    def get_system_user(self):
        return  ChatUser.objects.get_or_create(
            email='system@example.com',
            defaults={'name': 'System User', 'phone_number': '1234567890'}  # Add default values as necessary
        )

    @sync_to_async
    def generate_system_response(self, message):
        responses = SystemResponse.objects.all()
        for response in responses:
            if response.keyword in message.lower():
                return response.response
        return 'I am not sure how to respond to that.'
    
    def sanitize_group_name(self, group_name):
        # Sanitize the group name to only include allowed characters
        return re.sub(r'[^a-zA-Z0-9-_\.]', '_', group_name)
    

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'room_updates'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send_all_rooms()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def new_room_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def room_offline(self, event):
        await self.send(text_data=json.dumps(event))

    async def room_online(self, event):
        await self.send(text_data=json.dumps(event))

    async def new_message_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def send_all_rooms(self):
        rooms = await self.get_sorted_rooms()

        room_data = []
        for room in rooms:
            user_name = await self.get_user_name(room)
            last_message = await self.get_last_message(room)

            room_data.append({
                'room_id': room.id,
                'email': room.email,
                'user': user_name,
                'is_online': room.is_online,
                'created_at': room.created_at.isoformat(),
                'last_message_time': room.last_message_time.isoformat() if room.last_message_time else None,
                'last_message': last_message,
            })

        await self.send(text_data=json.dumps({
            'type': 'all_rooms',
            'rooms': room_data,
        }))

    @sync_to_async
    def get_sorted_rooms(self):
        return list(Room.objects.all().order_by('-last_message_time'))

    @sync_to_async
    def get_user_name(self, room):
        return room.user.name

    @sync_to_async
    def get_last_message(self, room):
        last_message = room.messages.order_by('-timestamp').first()
        return last_message.content if last_message else None
