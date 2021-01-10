""" Auth views. """

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

# Serializers
from api.users.serializers.auth import (
    SignupSerializer,
    LoginSerializer,
    EmailConfirmationSerializer
)

# Utilities
from typing import Union

# Serializer types
SerializersTypes = Union[
    SignupSerializer,
    LoginSerializer,
    EmailConfirmationSerializer
]


class AuthViews(viewsets.GenericViewSet):
    """ Auth views class. """

    def get_serializer_class(self) -> SerializersTypes:
        """ Get serializer class. """

        if self.action == 'signup':
            return SignupSerializer
        elif self.action == 'login':
            return LoginSerializer
        else:
            return EmailConfirmationSerializer

    @action(detail=False, methods=['post'])
    def signup(self, request: Request) -> Response:
        """ Signup view. """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.create(serializer.validated_data),
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def login(self, request: Request) -> Response:
        """ Login view. """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.create(),
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['patch'], url_path='email-confirmation')
    def email_confirmation(self, request: Request) -> Response:
        """ Email confirmation view. """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.update(serializer.validated_data),
            status=status.HTTP_200_OK
        )
