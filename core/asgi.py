import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from shop.consumers import OrderConsumer

import chat.routing
import web.routing
import shop.routing
import logge.routing
import webchat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns+
            web.routing.websocket_urlpatterns+
            shop.routing.shop_notification+
            logge.routing.websocket_urlpatterns+
            webchat.routing.websocket_urlpatternschat
            
        )
    ),
})
