from django.apps import AppConfig


class LoggeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logge'

    def ready(self):
        import logge.signal
