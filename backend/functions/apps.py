from django.apps import AppConfig


class FunctionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'functions'
    verbose_name = 'Функции'

    def ready(self):
        import functions.signals
