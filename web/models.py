# myapp/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from notificat.notification import *



class SiteStatus(models.Model):
    status = models.CharField(max_length=10, default='active')  # 'active' or 'paused'
    message = models.TextField(blank=True, null=True)

# models.py
class CustomUser(AbstractUser):
    # Add an 'is_online' field
    is_online = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # You can use any suitable name here
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # You can use any suitable name here
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )


class UserAccess(models.Model):
    ip_address = models.GenericIPAddressField(default=None, null=True)
    location = models.CharField(null=True, max_length=100)
    access_time = models.DateTimeField(auto_now_add=True)
    referer = models.URLField(null=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Add this field

    def __str__(self):
        return f"{self.ip_address} - {self.access_time}"

    # Add more fields if needed


class VisitorEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class simage(models.Model):
    image = models.FileField(upload_to='images/')
  

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    simage = models.ManyToManyField(simage, default=None)
    image = models.ImageField(upload_to='services/')
    price = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class data(models.Model):
    json_data = models.JSONField()

class image(models.Model):
    image = models.ImageField(upload_to='images/')
    width = models.PositiveIntegerField(default=400)
    height = models.PositiveIntegerField(default= 700)


class Order(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Order #{self.pk} - {self.service.title}"
     
class message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    about = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()


    def __str__(self):
        return f"Order #{self.pk}"

#------------- new models -------------
class Client_image(models.Model):
    width = models.PositiveIntegerField(default=0, help_text="Width of the image in pixels")
    height = models.PositiveIntegerField(default=0, help_text="Height of the image in pixels")


class Client(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='client_images/')

    def __str__(self):
        return self.name
    

class socilamedia(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class socilamedia_company(models.Model):
    social_media = models.ForeignKey(socilamedia, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)


class socilamedia_worker(models.Model):
    social_media = models.ForeignKey(socilamedia, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)


class worker_image(models.Model):
    width = models.PositiveIntegerField(default=0, help_text="Width of the image in pixels")
    height = models.PositiveIntegerField(default=0, help_text="Height of the image in pixels")

class worker(models.Model):
    postion = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    socilamedia_worker = models.ManyToManyField(socilamedia_worker, default=None)
    image = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class CompanyContact(models.Model):
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.company_name
    
class testmoni_image(models.Model):
    width = models.PositiveIntegerField(default=0, help_text="Width of the image in pixels")
    height = models.PositiveIntegerField(default=0, help_text="Height of the image in pixels")


class testmone(models.Model):
    name = models.CharField(max_length=100)
    postion = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class map(models.Model):
    link = models.CharField(max_length=1000)
    

class fuchers(models.Model):
    chat = models.BooleanField(default=False)
    message = models.BooleanField(default=False)
    testmonial = models.BooleanField(default=False)
    service = models.BooleanField(default=False)
    oneprodact = models.BooleanField(default=False)
    prodact = models.BooleanField(default=False)
    blog = models.BooleanField(default=False)
    social = models.BooleanField(default=False)
    worker = models.BooleanField(default=False)
    booking = models.BooleanField(default=False)
    about = models.BooleanField(default=False)  #Subscribers
    contact = models.BooleanField(default=False)
    map = models.BooleanField(default=False)
    sass = models.BooleanField(default=False)
    faq = models.BooleanField(default=False)
    galry = models.BooleanField(default=False)
    project = models.BooleanField(default=False)
    news = models.BooleanField(default=False)
    orderservice = models.BooleanField(default=False)
    email = models.BooleanField(default=False)



class Link(models.Model):
    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)  # Unique ID for the link
    url = models.URLField(null=True, blank=True)  # The URL to be accessed
    access_count = models.PositiveIntegerField(default=0)  # Access count
    prodact = models.BooleanField(default=False)
    redirect = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class galry_image(models.Model):
    width = models.PositiveIntegerField(default=0, help_text="Width of the image in pixels")
    height = models.PositiveIntegerField(default=0, help_text="Height of the image in pixels")

#FAQ 
class gtype(models.Model):    
    name = models.TextField(max_length=36, blank=True, null=True)

# website image
class galry(models.Model):
    description = models.TextField()
    url = models.URLField(null=True, blank=True)  # The URL to be accessed
    gtype = models.ForeignKey(gtype, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='galry/', null=True)

#FAQ 
class faq(models.Model):    
    qus = models.TextField(blank=True, null=True)
    ans = models.TextField(blank=True, null=True)


class appToken(models.Model):
  token = models.CharField(max_length=255)