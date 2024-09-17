# chat/migrations/000X_add_system_user.py

from django.db import migrations

def create_system_user(apps, schema_editor):
    ChatUser = apps.get_model('webchat', 'ChatUser')
    SystemResponse = apps.get_model('webchat', 'SystemResponse')
    
    # Create the system user
    system_user = ChatUser.objects.create(name='System', email='system@example.com', phone_number='0000000000')

    # Add predefined responses
    responses = [
        ('hello', 'Hello! How can I assist you today?'),
        ('help', 'Sure, I am here to help. Please tell me more.'),
        ('bye', 'Goodbye! Have a nice day!'),
    ]

    for keyword, response in responses:
        SystemResponse.objects.create(keyword=keyword, response=response)

class Migration(migrations.Migration):
    dependencies = [
        ('webchat', '0002_systemresponse'),
    ]

    operations = [
        migrations.RunPython(create_system_user),
    ]
