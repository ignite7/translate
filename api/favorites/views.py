""" Favorites views. """

# Dajngo REST framework
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

# Models
from api.users.models.users import UserModel

# Serializers
from api.favorites.serializers.favorites import FavoriteSerializer

# Permission
from api.utils.permissions import IsOwner


class FavoriteViews(viewsets.GenericViewSet):
    """ Favorites views class. """

    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = FavoriteSerializer
    queryset = UserModel.objects.filter(is_active=True, is_used=True)
    lookup_field = 'username'

    def retrieve(self, request: Request, **kwargs: dict) -> Response:
        """ Get favorites items of the user. """

        serializer = self.serializer_class(context={'request': request})

        return Response(
            data=serializer.retrieve(),
            status=status.HTTP_200_OK
        )

    def create(self, request: Request, **kwargs: dict) -> Response:
        """ Delete all and delete by id favorites items. """

        serializer = self.serializer_class(
            context={'request': request, 'uuid': kwargs['uuid']}
        )

        return Response(
            data=serializer.create(),
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request: Request, **kwargs: dict) -> Response:
        """ Delete all and delete by id favorites items. """

        serializer = self.serializer_class(
            context={'request': request, 'uuid': kwargs['uuid']}
        )

        return Response(
            data=serializer.delete(),
            status=status.HTTP_204_NO_CONTENT
        )

    def destroy_all(self, request: Request, **kwargs: dict) -> Response:
        """ Delete all favorites items. """

        serializer = self.serializer_class(context={'request': request})

        # Return delete all
        return Response(
            data=serializer.delete_all(),
            status=status.HTTP_204_NO_CONTENT
        )
