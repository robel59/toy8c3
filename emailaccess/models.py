from django.db import models
from django.conf import settings

class ZohoMailAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email =  models.CharField(max_length=255, null=True, blank=True)
    account_id =  models.CharField(max_length=255, null=True, blank=True)
    zoho_refresh_token = models.CharField(max_length=255)
    zoho_refresh_folder = models.CharField(max_length=255, null=True)
    zoho_email = models.EmailField(unique=True)
    client_id = models.CharField(max_length=555, null=True, blank=True)
    client_secr = models.CharField(max_length=555, null=True, blank=True)
    sent_folder_id = models.CharField(max_length=255, null=True, blank=True)
    inbox_folder_id = models.CharField(max_length=255, null=True, blank=True)
    redirect_uri = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.zoho_email


class new_email(models.Model):
    subject =models.TextField()
    fromm = models.CharField(max_length=100)  # Model name
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject