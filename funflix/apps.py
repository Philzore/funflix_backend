from django.apps import AppConfig


class FunflixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'funflix'

    def ready(self) -> None:
        from . import signals
