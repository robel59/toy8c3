from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from chat.models import *  # Import your Room model
from datetime import datetime
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import m2m_changed

from blog.models import *
from hotel.models import *
from sass.models import *
from shop import models as kol
from logge.consumer import VisitorInfoConsumer


@receiver(post_save, sender=User)
def create_chat_room(sender, instance, created, **kwargs):
    if created:
        room_name = instance.id
        Room.objects.create(name=room_name)


@receiver(user_logged_in)
def activate_chat_room(sender, request, user, **kwargs):
    user.is_online = True
    user.save()
    try:
        room = Room.objects.get(name=user.id)
        room.join(user)
    except Room.DoesNotExist:
        room_name = user.id
        room = Room.objects.create(name=room_name)
        room.join(user)

    channel_layer = get_channel_layer()
    print("ssssssssss")
    print(user.email)
    async_to_sync(channel_layer.group_send)(
        "user_access",
        {
            'type': 'message_notification',
            'roomid':room.name,
            'message': f"Login user:  {user.first_name}"
        }
    )   

@receiver(user_logged_out)
def update_last_login(sender, request, user, **kwargs):
    print("%%%%%%%%%%%%%%%%%%%%%%%%")
    user.room_set.update(last_login=datetime.now())

'''
@receiver(post_save, sender=UserAccess)
def user_access_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "user_access",
            {
                'type': 'user_access_notification',
                'message': f"New UserAccess created from IP {instance.ip_address}"
            }
        )'''


@receiver(post_save, sender=VisitorEmail)
def visitor_email_created(sender, instance, created, **kwargs):
    print("hhhhhhh")
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "user_access",
            {
                'type': 'new_subscription_notification',
                'message': f"Email added: {instance.email}"
            }
        )
'''
@receiver(post_save, sender=kol.Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "user_access",
            {
                'type': 'new_order_notification',
                'message': f"New Order : {instance.name}, for {instance.service}"
            }
        )    



@receiver(post_save, sender=kol.Order_chart)
def cart_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "user_access",
            {
                'type': 'new_order_notification',
                'message': f"Client : {instance.client.guest_name}, selected item {instance.service}"
            }
        )   
'''

@receiver(post_save, sender=Message)
def new_message(sender, instance, created, **kwargs):
    if created:
        if instance.user.is_superuser:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "user_access",
                {
                    'type': 'message_notification',
                    'roomid':instance.room.name,
                    'message': f"{instance.content}, form:  {instance.user.first_name}"
                }
            )   


@receiver(post_save, sender=Comment)
def new_comment(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "user_access",
            {
                'type': 'comment_notification',
                'message': f"{instance.name}, commented:  {instance.message} . on {instance.date_posted}"
            }
        ) 


@receiver(post_save, sender=Blog)
def new_read(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "user_access",
        {
            'type': 'read_notification',
            'message': f" new reader {instance.reads}"
        }
    ) 


@receiver(post_save, sender=Booking)
def new_booking(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "user_access",
            {
                'type': 'Booking_notification',
                'message': f"Booking order {instance.client.guest_name} from {instance.check_in_date} to {instance.check_out_date} for room type {instance.room_type.name}"
            }
        ) 


@receiver(post_save, sender=Subscription)
def new_sass(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "user_access",
            {
                'type': 'sass_notification',
                'message': f"SASS order {instance.user.name} for {instance.plan.name} on {instance.created_at}"
            }
        ) 

@receiver(post_save, sender=kol.Order)
def new_shop(sender, instance, **kwargs):
    print("HHHHHHHHH")
    if instance.active:
        try:
            user = User.objects.get(id = 1)
            user.is_online = True
            user.save()
            print(user)
            try:
                room = Room.objects.get(name=user.id)
                room.join(user)
            except Room.DoesNotExist:
                room_name = user.id
                room = Room.objects.create(name=room_name)
                room.join(user)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "order_notification",
                {
                    'type': 'message_notification',
                    'message':{'message': f"{instance.Client.guest_name} pick {instance.item.name} quantity  {instance.quntity}"}
                }

            ) 
        except User.DoesNotExist:
            pass
 


@receiver(post_save, sender=kol.Payment)
def new_shop(sender, instance, **kwargs):
    print("HHHHHHHHH")
    try:
        user = User.objects.get(id = 1)
        user.is_online = True
        user.save()
        print(user)
        try:
            room = Room.objects.get(name=user.id)
            room.join(user)
        except Room.DoesNotExist:
            room_name = user.id
            room = Room.objects.create(name=room_name)
            room.join(user)


        desc = 0
        disclist = []
        ord = instance.Order_chart
        ord.active = False
        ord.save()
        for dis in ord.coupons.all():
            desc = desc + dis.discount_amount
            disclist.append(dis)
        
        ordite = ord.order.all() #Order.objects.filter(Client = cli,active = True, sold = False )
        cost = 0
        ite = []
        for i in ordite:
            i.active = False
            i.save()
            cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
            io = [i,i.quntity * i.item.price ]
            ite.append(io)

        subtot = round(cost-desc, 2)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "order_notification",
            {
                'type': 'message_notification',
                'message':{'message': f"{instance.Client.guest_name} ready to pay for order number  {instance.Order_chart.id} ammount  {subtot} birr"}
            }

        ) 
    except User.DoesNotExist:
        pass


@receiver(m2m_changed, sender=kol.Payment.recipts.through)
def payment_receipts_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        print(f"Receipts added to Payment {instance.id}")
        try:
            user = User.objects.get(id = 1)
            user.is_online = True
            user.save()
            print(user)
            try:
                room = Room.objects.get(name=user.id)
                room.join(user)
            except Room.DoesNotExist:
                room_name = user.id
                room = Room.objects.create(name=room_name)
                room.join(user)


            desc = 0
            disclist = []
            ord = instance.Order_chart
            ord.active = False
            ord.save()
            for dis in ord.coupons.all():
                desc = desc + dis.discount_amount
                disclist.append(dis)
            
            ordite = ord.order.all() #Order.objects.filter(Client = cli,active = True, sold = False )
            cost = 0
            ite = []
            for i in ordite:
                i.active = False
                i.save()
                cost = cost + (i.quntity * i.item.price * (1-i.item.disc/100))
                io = [i,i.quntity * i.item.price ]
                ite.append(io)

            subtot = round(cost-desc, 2)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "order_notification",
                {
                    'type': 'message_notification',
                    'message':{'message': f"{instance.Client.guest_name} send you bank recipt for order number  {instance.Order_chart.id} ammount  {subtot} birr"}
                }

            ) 
        except User.DoesNotExist:
            pass

        # Perform additional actions as needed
    elif action == 'post_remove':
        print(f"Receipts removed from Payment {instance.id}")
        # Perform additional actions as needed