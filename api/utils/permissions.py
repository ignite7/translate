""" Commons permissions. """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Is owner permission class. """

    message = 'Not authorized for this action.'

    def has_permission(self, request, view):
        """ Check token and username are correct. """

        return request.user.username == view.kwargs['username']
