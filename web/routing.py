from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/user_access/$', consumers.UserAccessConsumer.as_asgi()),
    re_path(r'ws/ordernotification/$', consumers.OrderNotification.as_asgi()),
]
