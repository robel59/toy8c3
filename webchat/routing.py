# chat/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatternschat = [
    re_path(r'ws/webchat/(?P<email>[\w\.-]+@[\w\.-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/room-updates/$', consumers.RoomConsumer.as_asgi()),

]
