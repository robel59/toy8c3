# Generated by Django 4.2.4 on 2024-07-13 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='images/')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('data', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PageData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=255)),
                ('template_location', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('images', models.ManyToManyField(related_name='pages', to='webpage.imagefile')),
                ('languages', models.ManyToManyField(related_name='pages', to='webpage.language')),
            ],
        ),
        migrations.CreateModel(
            name='PageTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_data', models.JSONField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='webpage.language')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='webpage.pagedata')),
            ],
            options={
                'unique_together': {('page', 'language')},
            },
        ),
    ]