# backends.py

from django.contrib.auth.backends import ModelBackend
from .models import Client

class ClientBackend(ModelBackend):
    def authenticate(self, request, guest_email=None, guest_phone=None, password=None, **kwargs):
        try:
            # Try to find a user based on guest_email or guest_phone
            user = Client.objects.get(guest_email=guest_email) if guest_email else None
            user = user or Client.objects.get(guest_phone=guest_phone) if guest_phone else None
        except Client.DoesNotExist:
            user = None

        if user and user.check_password(password):
            return user

        return None
