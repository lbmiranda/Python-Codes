from django.apps import AppConfig

class AppdoacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appdoacoes'

    def ready(self):
        import appdoacoes.signals
