""" Favorites urls. """

# Django
from django.urls import path

# views
from api.favorites.views import FavoriteViews


urlpatterns = [
    path(
        route=r'<slug:username>/<uuid:uuid>',
        view=FavoriteViews.as_view(
            {'post': 'create', 'delete': 'destroy'}
        ),
        name='create_or_destroy_favorites'
    ),
    path(
        route='<slug:username>',
        view=FavoriteViews.as_view(
            {'get': 'retrieve', 'delete': 'destroy_all'}
        ),
        name='retrive_favorites'
    ),

]
