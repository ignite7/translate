""" Histories views. """

# Dajngo REST framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

# Models
from api.users.models.users import UserModel

# Serializers
from api.histories.serializers.histories import HistorySerializer

# Permissions
from api.utils.permissions import IsOwner


class HistoryViews(viewsets.GenericViewSet):
    """ History view class. """

    permission_classes = [IsAuthenticated, IsOwner]
    queryset = UserModel.objects.filter(is_active=True, is_used=True)
    serializer_class = HistorySerializer
    lookup_field = 'username'

    def get(self, request: Request, **kwargs: dict) -> Response:
        """ Get the histories of the user. """

        serializer = self.serializer_class(context={'request': request})

        return Response(
            data=serializer.retrieve(),
            status=status.HTTP_200_OK
        )

    def delete(self, request: Request, **kwargs: dict) -> Response:
        """ Delete specific history of the user. """

        serializer = self.serializer_class(
            context={'request': request, 'uuid': kwargs.get('uuid', None)}
        )

        if kwargs.get('uuid', False):
            return Response(
                data=serializer.delete(),
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            data=serializer.delete_all(),
            status=status.HTTP_204_NO_CONTENT
        )
