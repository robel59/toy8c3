from django.contrib import admin
from .models import ChatUser, Message, Room

@admin.register(ChatUser)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'content', 'timestamp')
    list_filter = ('room',)
    search_fields = ('content',)


admin.site.register(Room)

