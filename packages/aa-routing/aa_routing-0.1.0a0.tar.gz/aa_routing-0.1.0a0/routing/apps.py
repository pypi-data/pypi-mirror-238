from django.apps import AppConfig

from . import __version__


class RoutingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "routing"
    verbose_name = f'AA Routing v{__version__}'
