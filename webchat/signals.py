# signals.py
from datetime import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


    

@receiver(post_save, sender=Room)
def broadcast_new_room(sender, instance, created, **kwargs):

    if created:
        print("room created")
        name = ChatUser.objects.get(email = instance.email).name
        async_to_sync(channel_layer.group_send)(
            'room_updates',
            {
                'type': 'new_room_update',
                'room_id': instance.id,
                'name': instance.user.name,
                'email': instance.email,
                'user': instance.user.name,
                'is_online': instance.is_online,
                'last_message': "No Message",
                'created_at': instance.created_at.isoformat(),
                'last_message_time': instance.last_message_time.isoformat() if instance.last_message_time else None,
            }
        )
    else:
        if instance.is_online == False:
            async_to_sync(channel_layer.group_send)(
                'room_updates',
                {
                    'type': 'room_offline',
                    'room_id': instance.id,
                    'name': instance.user.name,
                    'email': instance.email,
                    'user': instance.user.name,
                    'is_online': instance.is_online,
                }
            )
        else:
            async_to_sync(channel_layer.group_send)(
                'room_updates',
                {
                    'type': 'room_online',
                    'room_id': instance.id,
                    'name': instance.user.name,
                    'email': instance.email,
                    'user': instance.user.name,
                    'is_online': instance.is_online,
                }
            )

    

@receiver(post_save, sender=Message)
def broadcast_new_message(sender, instance, created, **kwargs):
    if created:
        room = instance.room
        room.last_message_time = timezone.now()
        room.save()
        
        async_to_sync(channel_layer.group_send)(
            'room_updates',
            {
                'type': 'new_message_update',
                'room_id': room.id,
                'name': instance.user.name,
                'email': room.email,
                'user': room.user.name,
                'is_online': room.is_online,
                'is_online': instance.is_user,
                'last_message_time': room.last_message_time.isoformat(),
                'message': instance.content,
            }
        )
