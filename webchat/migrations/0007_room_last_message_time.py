# Generated by Django 4.2.4 on 2024-06-12 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webchat', '0006_room_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='last_message_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]