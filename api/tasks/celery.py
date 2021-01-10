""" Celery app config. """

# Django
from django.apps import apps, AppConfig
from django.conf import settings

# Utilities
import os

# Celery
from celery import Celery
from celery.schedules import crontab

# Settings
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

# App
app = Celery('api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'clean_ec_and_ia_tokens': {
        'task': 'clean ec and ia tokens',
        'schedule': crontab(hour=0)
    },
    'clean_rp_tokens': {
        'task': 'clean rp tokens',
        'schedule': crontab(hour=3)
    },
}


class CeleryAppConfig(AppConfig):
    """ Celery app config class. """

    name = 'api.tasks'
    verbose_name = 'Celery config'

    def ready(self) -> None:
        """ Discover tasks. """

        installed_apps = [
            app_config.name for app_config in apps.get_app_configs()
        ]
        app.autodiscover_tasks(lambda: installed_apps, force=True)
