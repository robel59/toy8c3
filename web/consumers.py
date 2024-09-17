from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs


class UserAccessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Add the user to a group to broadcast the notifications
        await self.channel_layer.group_add("user_access", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("user_access", self.channel_name)

    async def user_access_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type':"notifay",'message': message}))

    async def new_subscription_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type':"notifay", "title":"new subscription",'message': message}))

    async def new_order_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type':"notifay","title":"new order",'message': message}))

    async def message_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type':"new_message","title":"new message","room":event['roomid'],'message': message}))

    async def login_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type':"new_message","title":"new login","room":event['roomid'],'message': message}))



class OrderNotification(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("order_notification", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("order_notification", self.channel_name)

    async def receive(self, text_data):
        # Handle received data (if needed)
        pass

    async def message_notification(self, event):
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps(event['message']))