from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(RoomType)
admin.site.register(Description)
admin.site.register(ImageSize)
admin.site.register(Image)
admin.site.register(Client)
admin.site.register(Booking)
