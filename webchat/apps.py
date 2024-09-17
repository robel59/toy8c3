from django.apps import AppConfig


class WebchatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webchat'


    def ready(self):
        import webchat.signals
