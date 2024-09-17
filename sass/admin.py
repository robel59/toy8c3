from django.contrib import admin

# Register your models here.
# myapp/admin.py
from django.contrib import admin
from .models import *

admin.site.register(Offer)
admin.site.register(SASSClient)
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
