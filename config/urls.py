""" Config urls """

# Django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # Translate
    path(
        '',
        include(
            ('api.translations.urls', 'translations'),
            namespace='translations'
        )
    ),

    # History
    path(
        '',
        include(
            ('api.histories.urls', 'histories'),
            namespace='histories'
        )
    ),

    # Favorites
    path(
        'favorites/',
        include(
            ('api.favorites.urls', 'favorites'),
            namespace='favorites'
        )
    ),

    # Users
    path(
        '',
        include(
            ('api.users.urls', 'users'),
            namespace='users'
        )
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
