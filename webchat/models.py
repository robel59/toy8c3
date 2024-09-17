from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class ChatUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    is_team_member = models.BooleanField(default=False)  # Add this field to differentiate team members

    def __str__(self):
        return self.name

class Room(models.Model):
    email = models.EmailField(unique=True)
    user = models.ForeignKey('ChatUser', on_delete=models.CASCADE, related_name='rooms')
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Room for {self.user.email}'
    
    def set_online_state(self, is_online):
        self.is_online = is_online
        self.save(update_fields=['is_online'])

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_user = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name}: {self.content[:50]}'

class SystemResponse(models.Model):
    keyword = models.CharField(max_length=100)
    response = models.TextField()

    def __str__(self):
        return f'Keyword: {self.keyword}, Response: {self.response[:50]}'
