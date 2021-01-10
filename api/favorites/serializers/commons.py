""" Commons favorites serializers. """

# Django REST framwork
from rest_framework import serializers

# Models
from api.histories.models import (
    HistoryTranslationsModel,
    HistoryIdentifyModel
)


class FavoriteTranslationsSerializer(serializers.ModelSerializer):
    """ Favorite translate serializer class. """

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
        )


class FavoriteIdenfySerializer(serializers.ModelSerializer):
    """ Favorite identify serializer class. """

    id = serializers.UUIDField(source='pk')
    message = serializers.CharField(source='text')

    class Meta:
        """ Serializer fields. """

        model = HistoryIdentifyModel
        fields = (
            'id',
            'message',
            'identify_languages',
        )
