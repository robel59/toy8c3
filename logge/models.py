# myapp/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Log(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)  # Model name
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.type} on {self.date}"


@receiver(post_save, sender=Log)
def log_saved(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "log_group",
        {
            "type": "log_message",
            "message": {
                "title": instance.title,
                "type": instance.type,
                "message": instance.message,
                "date": instance.date.isoformat(),
            },
        },
    )
