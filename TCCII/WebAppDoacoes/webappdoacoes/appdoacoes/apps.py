from django.apps import AppConfig

class AppdoacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appdoacoes'

    # def ready(self):
    #     from django.contrib.auth import get_user_model
    #     User = get_user_model()
    #     if not User._meta.swapped:
    #         from django.conf import settings
    #         settings.AUTH_USER_MODEL = 'appdoacoes.User'