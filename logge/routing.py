from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/logs/$', consumer.LogConsumer.as_asgi()),
    re_path(r'ws/online/', consumer.OnlineUserConsumer.as_asgi()),
    re_path(r'ws/visitor_info/$', consumer.VisitorInfoConsumer.as_asgi()),
    re_path(r'ws/chart_data/$', consumer.ChartDataConsumer.as_asgi()),
    re_path(r'ws/user_access123/$', consumer.UserAccessConsumer.as_asgi()),


]
