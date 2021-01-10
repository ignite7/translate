""" Commons translations serializers. """

# Django REST framework
from rest_framework import serializers

# Models
from api.histories.models import (
    HistoryTranslationsModel,
    HistoryIdentifyModel
)


class HistoryModelSerializer(serializers.Serializer):
    """ History model serializer class. """

    message = serializers.CharField(
        max_length=51.200,
        label='Message',
        help_text='Message field'
    )

    favorite = serializers.BooleanField(
        default=False,
        label='Save to favorites',
        help_text='Favorite field.'
    )

    def validate(self, attrs: dict) -> dict:
        """ Validate empty data. """

        # Not blanks fields
        if len(attrs['message']) == 0:
            raise serializers.ValidationError('Not blank fields.')

        return attrs


class HistoryTranslationsModelSerializer(serializers.ModelSerializer):
    """ History translation model serializer class. """

    message = serializers.CharField(
        max_length=51.200,
        source='text'
    )

    class Meta:
        """ Override meta class. """

        model = HistoryTranslationsModel
        fields = (
            'message',
            'source',
            'target',
            'translation',
            'word_count',
            'character_count',
        )


class HistoryIdentifyModelSerializer(serializers.ModelSerializer):
    """ Hsitory identify model serializer class. """

    message = serializers.CharField(
        max_length=51.200,
        source='text'
    )

    class Meta:
        """ Override meta class. """

        model = HistoryIdentifyModel
        fields = (
            'message',
            'identify_languages',
        )
