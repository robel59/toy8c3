from datetime import datetime, timedelta
import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

from web.models import UserAccess, Link
from .models import *
from asgiref.sync import sync_to_async
from django.core.cache import cache
from webchat.models import Room
from channels.db import database_sync_to_async
import datetime
from shop.models import Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncMonth


class UserAccessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("user_access_group", self.channel_name)
        await self.accept()

        # Send initial data
        await self.send_user_access_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("user_access_group", self.channel_name)

    async def receive(self, text_data):
        pass

    @sync_to_async
    def get_user_access_data(self):
        one_year_ago = timezone.now() - datetime.timedelta(days=365)
        user_access_data = UserAccess.objects.filter(access_time__gte=one_year_ago) \
            .annotate(month=TruncMonth('access_time')) \
            .values('month') \
            .annotate(count=Count('id')) \
            .values('month', 'count') \
            .order_by('month')

        # Convert datetime to string
        for item in user_access_data:
            item['month'] = item['month'].strftime('%Y-%m')

        return list(user_access_data)

    async def send_user_access_data(self):
        data = await self.get_user_access_data()
        await self.send(text_data=json.dumps({"user_access_data": data}))

    async def user_access_message(self, event):
        await self.send_user_access_data()


def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


class ChartDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chart_data'
        self.room_group_name = 'chart_data_group'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send_initial_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_initial_data(self):
        data = await self.get_chart_data()
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_chart_data(self):
        link_data = Link.objects.values('name', 'access_count', 'prodact')
        order_data = Order.objects.values('item__name').annotate(total_quantity=models.Sum('quntity'))

        link_chart_data = []
        for link in link_data:
            link_chart_data.append({
                'name': link['name'],
                'value': link['access_count'],
                'color': generate_random_color(),#'#color_code_based_on_some_logic'  # Define logic for color coding
            })

        order_chart_data = []
        for order in order_data:
            order_chart_data.append({
                'name': order['item__name'],
                'value': order['total_quantity'],
                'color': generate_random_color()#'#color_code_based_on_some_logic'  # Define logic for color coding
            })

        return {
            'link_chart_data': link_chart_data,
            'order_chart_data': order_chart_data
        }

    @staticmethod
    async def broadcast_chart_data():
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'chart_data_group',
            {
                'type': 'chart_data_message'
            }
        )

    async def chart_data_message(self, event):
        data = await self.get_chart_data()
        await self.send(text_data=json.dumps(data))


class VisitorInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'visitor_info'
        self.room_group_name = 'visitor_info_group'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send initial visitor info
        await self.send_visitor_info()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # This consumer does not handle received messages
        pass

    @database_sync_to_async
    def get_visitor_info(self):
        online_users = Room.objects.filter(is_online=True).count()
        total_visitors = UserAccess.objects.count()
        today_visitors = UserAccess.objects.filter(access_time__date=datetime.date.today()).count()
        last_7_days_visitors = UserAccess.objects.filter(access_time__gte=datetime.datetime.now() - datetime.timedelta(days=7)).count()
        last_month_visitors = UserAccess.objects.filter(access_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).count()
        
        visitor_info = {
            'online_users': online_users,
            'total_visitors': total_visitors,
            'today_visitors': today_visitors,
            'last_7_days_visitors': last_7_days_visitors,
            'last_month_visitors': last_month_visitors,
        }

        return visitor_info

    async def send_visitor_info(self):
        visitor_info = await self.get_visitor_info()

        # Send message to WebSocket
        await self.send(text_data=json.dumps(visitor_info))

    @staticmethod
    def broadcast_visitor_info():
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'visitor_info_group',
            {
                'type': 'visitor_info_message',
            }
        )

    async def visitor_info_message(self, event):
        # Send updated visitor info
        await self.send_visitor_info()

class OnlineUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Increment online user count
        await self.increment_online_users()
        await self.accept()

    async def disconnect(self, close_code):
        # Decrement online user count
        await self.decrement_online_users()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'get_online_users':
            today = datetime.now().date()
            last_7_days = today - timedelta(days=7)
            
            # Get counts asynchronously
            visitors_today = await self.get_visitors_today(today)
            visitors_last_7_days = await self.get_visitors_last_7_days(last_7_days)
            online_users = await self.get_online_users()
            
            # Send data back to the client
            await self.send(text_data=json.dumps({
                'online_users': online_users,
                'today': visitors_today,
                'week': visitors_last_7_days
            }))

    @sync_to_async
    def get_visitors_today(self, today):
        return UserAccess.objects.filter(access_time__date=today).count()

    @sync_to_async
    def get_visitors_last_7_days(self, last_7_days):
        return UserAccess.objects.filter(access_time__date__gte=last_7_days).count()

    @sync_to_async
    def increment_online_users(self):
        online_users = cache.get('online_users', 0)
        cache.set('online_users', online_users + 1)

    @sync_to_async
    def decrement_online_users(self):
        online_users = cache.get('online_users', 0)
        cache.set('online_users', max(0, online_users - 1))

    @sync_to_async
    def get_online_users(self):
        return cache.get('online_users', 0)


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "log_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "log_group",
            self.channel_name
        )

    
    async def log_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'get_last_logs':
            count = text_data_json.get('count', 15)  # Default to 15 if no count is provided
            await self.send_last_logs(count)
        else:
            # Handle other actions if necessary
            pass

    async def send_last_logs(self, count):
        last_logs = await self.get_last_logs(count)  # Await the async function
        logs_list = [
            {
                'title': log.title,
                'type': log.type,
                'message': log.message,
                'date': log.date.isoformat()  # Format the date for JSON
            } for log in last_logs
        ]
        await self.send(text_data=json.dumps({'logs': logs_list}))

    @sync_to_async
    def get_last_logs(self, count):
        # Synchronous function to fetch last 'count' logs
        return list(Log.objects.order_by('-date')[:count])
