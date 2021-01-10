""" Users urls. """

# Django
from django.urls import path
from django.urls.conf import include

# Django REST framework
from rest_framework.routers import DefaultRouter

# views
from api.users.views.auth import AuthViews
from api.users.views.accounts import (
    ResetPasswordViews,
    AccountViews
)


router = DefaultRouter(trailing_slash=False)
router.register(r'users', AuthViews, basename='auth')
urlpatterns = [
    path('', include(router.urls)),
    path(
        route='users/reset-password',
        view=ResetPasswordViews.as_view(),
        name='reset_password'
    ),
    path(
        route='users/<slug:username>',
        view=AccountViews.as_view({'get': 'retrieve', 'put': 'update'}),
        name='accounts'
    ),

]
