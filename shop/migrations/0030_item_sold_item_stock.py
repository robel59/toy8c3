# Generated by Django 4.2.4 on 2024-07-18 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_subcategorytype_remove_rating_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sold',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]