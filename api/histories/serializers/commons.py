""" History commons serializers. """

# Django REST framework
from django.utils import translation
from rest_framework import serializers

# Models
from api.histories.models import (
    HistoryTranslationsModel,
    HistoryIdentifyModel
)


class HistoryTranlationSerializer(serializers.ModelSerializer):
    """ History translation serializer class. """

    id = serializers.UUIDField(source='pk')
    message = serializers.CharField(source='text')

    class Meta:
        """ Serializer fields. """

        model = HistoryTranslationsModel
        fields = (
            'id',
            'message',
            'source',
            'target',
            'translation',
            'word_count',
            'character_count',
            'favorite',
        )


class HistoryIdenfySerializer(serializers.ModelSerializer):
    """ History identify serializer class. """

    id = serializers.UUIDField(source='pk')
    message = serializers.CharField(source='text')

    class Meta:
        """ Serializer fields. """

        model = HistoryIdentifyModel
        fields = (
            'id',
            'message',
            'identify_languages',
            'favorite'
        )
