from django.urls import path
from .views import list_inbox_emails, list_emails, get_email_content, get_email_parameters,zoho_mail_webhook

urlpatterns = [
    path('inbox/', list_inbox_emails, name='inbox_emails'),
    path('emails/', list_emails, name='list_emails'),
    path('email_parameters/', get_email_parameters, name='get_email_parameters'),
    path('email_content/<str:folder_id>/<str:message_id>/', get_email_content, name='get_email_content'),
    path('webhook/', zoho_mail_webhook, name='zoho_mail_webhook'),

]
