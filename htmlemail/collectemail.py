import re
from django.apps import apps

def collect_emails():
    email_addresses = set()
    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    # Iterate over all models
    for model in apps.get_models():
        # Check if the model has a field named 'email'
        if 'email' in [field.name for field in model._meta.get_fields()]:
            # Get all email addresses from this field
            email_values = model.objects.values_list('email', flat=True)
            for email in email_values:
                if isinstance(email, str) and email_regex.match(email):
                    email_addresses.add(email)

    # Convert set to list
    email_list = list(email_addresses)

    return email_list
