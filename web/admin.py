# myapp/admin.py
from django.contrib import admin
from .models import *

class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'location', 'access_time')
    list_filter = ('location', 'access_time')
    search_fields = ('ip_address', 'location')

admin.site.register(UserAccess, UserAccessAdmin)

class VisitorEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('email',)

admin.site.register(VisitorEmail, VisitorEmailAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')

admin.site.register(Service, ServiceAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('service', 'name', 'phone_number', 'email', 'created_at')
    list_filter = ('created_at', 'service')
    search_fields = ('name', 'phone_number', 'email')

admin.site.register(Order, OrderAdmin)

admin.site.register(image)
admin.site.register(data)
admin.site.register(simage)
admin.site.register(message)



admin.site.register(Client_image)
admin.site.register(Client)
admin.site.register(socilamedia)
admin.site.register(socilamedia_company)
admin.site.register(socilamedia_worker)
admin.site.register(worker)
admin.site.register(CompanyContact)
admin.site.register(testmone)
admin.site.register(map)
admin.site.register(fuchers)
admin.site.register(worker_image)
admin.site.register(testmoni_image)
admin.site.register(Link)
admin.site.register(galry)
admin.site.register(faq)
admin.site.register(appToken)
