# Generated by Django 4.2.4 on 2024-06-11 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webchat', '0003_add_system_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatuser',
            name='is_team_member',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='webchat.chatuser'),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='webchat.chatuser')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='webchat.room'),
            preserve_default=False,
        ),
    ]