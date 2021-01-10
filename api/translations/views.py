""" Translate views. """

# Dajngo REST framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

# Serializers
from api.translations.serializers.translations import TranslateSerializer
from api.translations.serializers.identify import IdentifySerializer

# Utilities
from typing import Union

# Serializers types
SerializersTypes = Union[
    TranslateSerializer,
    IdentifySerializer
]


class TranslateView(viewsets.GenericViewSet):
    """ Translate view class. """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> SerializersTypes:
        """ Get serializer class. """

        if self.action == 'translate':
            return TranslateSerializer
        else:
            return IdentifySerializer

    @action(detail=False, methods=['post'])
    def translate(self, request: Request) -> Response:
        """
        Translates the input text from the source
        language to the target language.
        """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.retrieve(serializer.validated_data),
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def identify(self, request: Request) -> Response:
        """ Identifies the language of the input text. """

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data or request.query_params,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.retrieve(serializer.validated_data),
            status=status.HTTP_200_OK
        )
