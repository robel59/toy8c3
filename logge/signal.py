# myapp/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from logge.consumer import ChartDataConsumer, VisitorInfoConsumer
from .models import Log
from django.apps import apps

# Import the models you want to log
from web.models import ( UserAccess, VisitorEmail, simage, Service, data, image, 
    Order, message, Client, socilamedia, socilamedia_company, 
    socilamedia_worker, worker, CompanyContact, testmoni_image, 
    testmone, map, Link, galry, faq, appToken
)

from webchat.models import Message, Room
from blogg.models import Blog, Comment
from emailaccess.models import new_email
from hotel import models as hote
from news import models as newss
from pro import models as proj
from sass.models import Offer, SASSClient, SubscriptionPlan, Subscription
from service import models as serv
from shop import models as sho
from notificat.notification import *
from asgiref.sync import async_to_sync



@receiver(post_save, sender=UserAccess)
@receiver(post_save, sender=Room)
def trigger_visitor_info_update(sender, instance, **kwargs):
    VisitorInfoConsumer.broadcast_visitor_info()

@receiver(post_save, sender=Link)
@receiver(post_save, sender=sho.Order)
def broadcast_chart_data(sender, instance, **kwargs):
    async_to_sync(ChartDataConsumer.broadcast_chart_data)()

# List of models to log
logged_models = [UserAccess, message, VisitorEmail, Order, Message, new_email, hote.Booking, Comment, newss.Comment, proj.Comment,
                 
    Service, data, image,  Client, socilamedia_company, worker, CompanyContact, testmone, map, 
    Link, galry, faq, Blog, hote.Client, hote.RoomType,newss.News,proj.Project,Offer, SASSClient, SubscriptionPlan, Subscription,serv.Service, serv.Order, 
    sho.Client, sho.Item,  sho.Order, sho.Coupon, sho.Order_chart, sho.Bank, sho.Payment
]

notified_models = [message, VisitorEmail, Order, Message, new_email,sho.Order, hote.Booking, Comment, newss.Comment, proj.Comment, serv.Order, Link]


# Logging function
def log_action(instance, action, sender):
    if(sender == UserAccess):
        model_name = f"New Vistor {instance.location}"
        action_message = f"IP {instance.ip_address}\n come from {instance.referer}"
    elif(sender == message):
        model_name = f"New Message form {instance.name}"
        action_message = f"{instance.about}\n {instance.description} \n {instance.email}"
    elif(sender == VisitorEmail):
        model_name = f"New Email Subscriber"
        action_message = f"Email : {instance.email}"
    elif(sender == Order):
        model_name = f"New Order for {instance.service.model_name}"
        action_message = f"Order by {instance.name}\nPhone : {instance.phone_number}\nEmail : {instance.email}"
    elif(sender == 'sho.Order'):
        model_name = f"New Order for {instance.name}"
        action_message = f"Order by {instance.name}\nPhone : {instance.phone_number}\nEmail : {instance.email}"
    elif(sender == Message):
        model_name = f"New Chat by {instance.user.name}"
        action_message = f"{instance.content}"
    elif(sender == new_email):
        model_name = f"New Email Subject : {instance.subject}"
        action_message = f"{instance.body}\n From : {instance.fromm}"
    elif(sender == hote.Booking):
        model_name = f"{instance.__class__.__name__} {action}"
        action_message = f"An entry has been {action.lower()}: {instance}"
    elif(sender == newss.Comment):
        model_name = f"New Comment for {instance.News.title} by {instance.name}"
        action_message = f"{instance.message}\n{instance.email}"
    elif(sender == proj.Comment):
        model_name = f"New Comment for {instance.Project.title} by {instance.name}"
        action_message = f"{instance.message}\n{instance.email}"
    elif(sender == Comment):
        model_name = f"New Comment for {instance.blog.title} by {instance.name}"
        action_message = f"{instance.message}\n{instance.email}"
    #---- to be edited -----
    elif(sender == Service):
        model_name = f"New Service ({instance.title})"
        action_message = f"{instance.description}"
    elif(sender == data):
        model_name = f"Website Text data updated"
        action_message = f"Website Text data updated"
    elif(sender == image):
        model_name = f"Website Image updated"
        action_message = f"Website Image updated"
    elif(sender == Client):
        model_name = f"New Partner for {instance.name}"
        action_message = f"name {instance.name}\nWebsite : {instance.website}"
    elif(sender == socilamedia_company):
        model_name = f"New Social media registered {instance.social_media.name}"
        action_message = f"{instance.link}"
    elif(sender == worker):
        model_name = f"New employee : {instance.name}"
        action_message = f"{instance.description}\n{instance.postion}"
    elif(sender == CompanyContact):
        model_name = f"company contact updated"
        action_message = f"{instance.company_name}\n{instance.address}\n{instance.address}\n{instance.phone_number}"
    elif(sender == testmone):
        model_name = f"Testimony updated {instance.name}"
        action_message = f"{instance.description}"
    elif(sender == map):
        model_name = f"Map updated"
        action_message = f"{instance.link}"
    elif(sender == Link):
        model_name = f"Web Link updated {instance.name}"
        action_message = f"link {instance.url}\nTotal Vister ({instance.access_count})"
    elif(sender == galry):
        model_name = f"website Galary updated"
        action_message = f"{instance.description}"
    elif(sender == faq):
        model_name = f"FAQ Q : {instance.qus}"
        action_message = f"A : {instance.ans}"
    elif(sender == Blog):
        model_name = f"Blog title : {instance.title}"
        action_message = f" {instance.description}\nAuther : {instance.author}\nRead : {instance.reads}"
    elif(sender == newss.News):
        model_name = f"News title : {instance.title}"
        action_message = f" {instance.description}\nAuther : {instance.author}\nRead : {instance.reads}"
    elif(sender == proj.Project):
        model_name = f"Project title : {instance.title}"
        action_message = f" {instance.description}\nAuther : {instance.author}\nRead : {instance.reads}"
    elif(sender == serv.Service):
        model_name = f"Service title : {instance.title}, Price : {instance.price}"
        action_message = f" {instance.description}\nRead : {instance.reads}"
    elif(sender == Offer):
        model_name = f"Offer updated {instance.name}"
        action_message = f"{instance.description}"
    elif(sender == SASSClient):
        model_name = f"New Client : {instance.name}"
        action_message = f"Phone : {instance.phone}\n Email : {instance.email}"
    elif(sender == SubscriptionPlan):
        model_name = f"Subscription plan Name : {instance.name}, Price : {instance.price}"
        action_message = f"{instance.description}"
    elif(sender == Subscription):
        model_name = f"New Subscription for {instance.plan.name} by {instance.user.name}"
        action_message = f"plan started at {instance.start_date} to {instance.end_date}\nClient Phone : {instance.user.phome}\nEmail : {instance.user.email}"
    elif(sender == serv.Order):
        model_name = f"New Order for {instance.service.title} by {instance.name}"
        action_message = f"plan selected at {instance.date}\nClient Phone : {instance.phone_number}\nEmail : {instance.email}"
    elif(sender == sho.Client):
        model_name = f"New Client {instance.guest_name} by {instance.user}" # need some can modification
        action_message = f"Phone : {instance.guest_phone}\nEmail : {instance.guest_email}"
    elif(sender == sho.Item):
        model_name = f"shop Producat updated( {instance.name}), Price : {instance.price}"
        action_message = f"{instance.descriptions}\nDiscount : {instance.disc}\n Is Active : {instance.active}"
    elif(sender == sho.Order):
        model_name = f"{instance.item.name} Cart Added by {instance.Client}"
        action_message = f"Phone : {instance.Client.guest_phone}\n Email : {instance.Client.guest_email} \n Active : {instance.active} \n Sold : {instance.sold}"
    elif(sender == sho.Order_chart):
        model_name = f"Order Client : {instance.client}"
        dataord = 'Name  --  price -- qunt'
        for i in instance.order.all():
            dataord = dataord + f"\n{i.item.name} -- {i.item.price} -- {i.quntity},"

        action_message = f"Item : \n{dataord}\nPhone : {instance.client.guest_phone}\n Email : {instance.client.guest_email}"
    
    else:
        model_name = instance.__class__.__name__
        action_message = f"{instance.__dict__}"

    log = Log(
        title=f"{model_name} ({action})",
        type=str(sender),  # Log the model name here
        message=action_message
    )
    log.save()

# Signal handler for save (create and update)
@receiver(post_save)
def create_or_update_log(sender, instance, created, **kwargs):
    if sender in logged_models:
        action = 'Created' if created else 'Updated'
        log_action(instance, action, sender)
    if sender in notified_models:
        print(sender)
        print("kkkkkkss3333")
        tokens_list = appToken.objects.all()
        #if(sender == UserAccess):
            #title = f"New Vistor {instance.location}"
            #message_body = f"IP {instance.ip_address}\n come from {instance.referer}"
        if(sender == Message):
            title = f"New Chat by {instance.user.name}"
            message_body = f"{instance.content}"
        elif(sender == message):
            title = f"New Message form {instance.name}"
            message_body = f"{instance.about}\n {instance.description} \n {instance.email}"
        elif(sender == VisitorEmail):
            title = f"New Email Subscriber"
            message_body = f"Email : {instance.email}"
        elif(sender == Order):
            title = f"New Order for {instance.service.title}"
            message_body = f"Order by {instance.name}\nPhone : {instance.phone_number}\nEmail : {instance.email}"
        elif(sender == 'sho.Order'):
            title = f"New Order for {instance.service.model_name}"
            message_body = f"Order by {instance.name}\nPhone : {instance.phone_number}\nEmail : {instance.email}"
        elif(sender == sho.Bank):
            title = f"Bank Account {instance.Bank_name}"
            message_body = f"Account Name {instance.name}\nAccount number : {instance.account_number}"
        elif(sender == sho.Payment):
            title = f"payment : {instance.subject}"
            message_body = f"{instance.body}\n From : {instance.fromm}"
        elif(sender == hote.Booking):
            title = f"{instance.__class__.__name__} {action}"
            message_body = f"An entry has been {action.lower()}: {instance}"
        elif(sender == newss.Comment):
            title = f"New Comment for {instance.News.title} by {instance.name}"
            message_body = f"{instance.message}\n{instance.email}"
        elif(sender == proj.Comment):
            title = f"New Comment for {instance.Project.title} by {instance.name}"
            message_body = f"{instance.message}\n{instance.email}"
        elif(sender == Comment):
            title = f"New Comment for {instance.blog.title} by {instance.name}"
            message_body = f"{instance.message}\n{instance.email}"
        elif(sender == Link):
            title = f"Web Link updated {instance.name}"
            message_body = f"link {instance.url}\nTotal Vister ({instance.access_count})"
        elif(sender == Subscription):
            title = f"New Subscription for {instance.plan.name} by {instance.user.name}"
            message_body = f"plan started at {instance.start_date} to {instance.end_date}\nClient Phone : {instance.user.phome}\nEmail : {instance.user.email}"
        elif(sender == sho.Order):
            title = f"{instance.item.name} Cart Added by {instance.Client}"
            message_body = f"Phone : {instance.Client.guest_phone}\n Email : {instance.Client.guest_email} \n Active : {instance.active} \n Sold : {instance.sold}"
        elif(sender == serv.Order):
            title = f"New Order for {instance.service.title} by {instance.name}"
            message_body = f"plan selected at {instance.date}\nClient Phone : {instance.phone_number}\nEmail : {instance.email}"
        elif(sender == sho.Order_chart):
            title = f"Order Client : {instance.client}"
            dataord = 'Name  --  price -- qunt'
            for i in instance.order:
                dataord = dataord + f"\n{i.order.item.name} -- {i.order.item.price} -- {instance.order.quntity},"

            message_body = f"Item : \n{dataord}\nPhone : {instance.client.guest_phone}\n Email : {instance.client.guest_email}"
    
        

        for i in tokens_list:
            print("pppp")
            sendNotfication(title, message_body, i.token)  # Replace 'recipient_token'


# Signal handler for delete
#@receiver(post_delete)
def delete_log(sender, instance, **kwargs):
    if sender in logged_models:
        log_action(instance, 'Deleted')
