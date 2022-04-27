from django.apps import AppConfig

class ProfbeatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Profbeats'

    def ready(self):
        import signals