""" User app. """

# Django
from django.apps import AppConfig


class UserAppConfig(AppConfig):
    """User app config."""

    name = 'api.users'
    verbose_name = 'Users'
