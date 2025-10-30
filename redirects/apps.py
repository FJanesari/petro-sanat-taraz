from django.apps import AppConfig


class RedirectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'redirects'
    verbose_name = 'ریدایرکت'

    def ready(self):
        import redirects.signals
