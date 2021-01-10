""" Histories urls. """

# Django REST framework
from rest_framework.routers import Route, SimpleRouter

# Views
from api.histories.views import HistoryViews


class CustomHistoryRoutes(SimpleRouter):
    """ Custom url routes. """

    routes = [
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'get'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/?(?P<uuid>[\w\d\-]+)?$',
            mapping={'delete': 'delete'},
            name='{basename}-delete',
            detail=True,
            initkwargs={'suffix': 'Delete'}
        ),
    ]


router = CustomHistoryRoutes(trailing_slash=False)
router.register(r'histories', HistoryViews, basename='histories')
urlpatterns = router.urls
