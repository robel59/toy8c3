
from .consumers import OrderConsumer
from django.urls import re_path




shop_notification = [
    re_path(r'ws/user_access/$', OrderConsumer.as_asgi()),
]