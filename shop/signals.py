from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json

from channels.layers import get_channel_layer
from .models import Order

@receiver(post_save, sender=Order)
def order_saved(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    # Send notification to the WebSocket group (all connected clients)
    async_to_sync(channel_layer.group_send)(
        "order_group",
        {
            "type": "order_notification",
            "message": json.dumps({"event": "order_saved", "order_id": instance.id}),
        },
    )
