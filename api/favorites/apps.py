""" Favorite app. """

# Django
from django.apps import AppConfig


class FavoriteAppConfig(AppConfig):
    """Favorite app config."""

    name = 'api.favorites'
    verbose_name = 'Favorites'
