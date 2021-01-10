""" Account view. """

# Django REST framework
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

# Serializers
from api.users.serializers.accounts import (
    GetAccountSerializer,
    UpdateAccountSerializer,
    SendResetPasswordSerializer,
    ResetPasswordSerializer
)

# Models
from api.users.models.users import UserModel

# Permissions
from api.utils.permissions import IsOwner

# Utilities
from typing import Union

# Serializer types
SerializersTypes = Union[
    GetAccountSerializer,
    UpdateAccountSerializer,
    SendResetPasswordSerializer,
    ResetPasswordSerializer
]


class AccountViews(viewsets.GenericViewSet):
    """ Account views class. """

    lookup_field = 'username'
    queryset = UserModel.objects.filter(verified_email=True, is_active=True)
    http_method_names = ['get', 'put']
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self) -> SerializersTypes:
        """ Get serializer class. """

        if self.request.method.lower() == 'get':
            return GetAccountSerializer
        else:
            return UpdateAccountSerializer

    def retrieve(self, request: Request, **kwargs: dict) -> Response:
        """ Get account details view. """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params,
            context={
                'request': request,
                'username': kwargs['username']
            }
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.retrieve(),
            status=status.HTTP_200_OK
        )

    def update(self, request: Request, **kwargs: dict) -> Response:
        """ Get account details view. """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params,
            context={
                'request': request,
                'username': kwargs['username']
            }
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.update(serializer.validated_data),
            status=status.HTTP_200_OK
        )


class ResetPasswordViews(APIView):
    """ Reset password views class. """

    http_method_names = ['post', 'patch']
    permission_classes = [AllowAny]

    def get_serializer_class(self) -> SerializersTypes:
        """ Get serializer class. """

        if self.request.method.lower() == 'post':
            return SendResetPasswordSerializer
        else:
            return ResetPasswordSerializer

    def post(self, request: Request) -> Response:
        """ Send Reset password view. """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.create(serializer.validated_data),
            status=status.HTTP_201_CREATED
        )

    def patch(self, request: Request) -> Response:
        """ Reset password view. """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.update(serializer.validated_data),
            status=status.HTTP_200_OK
        )
