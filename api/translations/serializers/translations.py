""" Translations serializers. """

# Django REST framework
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer

# Serializers
from api.translations.serializers.commons import (
    HistoryModelSerializer,
    HistoryTranslationsModelSerializer
)

# Models
from api.users.models.users import UserModel
from api.histories.models import HistoryTranslationsModel

# Utilities
import requests
import environ
from cli.utils.languages import languages_list

# Environ
env = environ.Env()
environ.Env.read_env()


class TranslateSerializer(HistoryModelSerializer):
    """ Translate serializer class. """

    source = serializers.ChoiceField(
        choices=languages_list,
        label='Source',
        help_text='Source field.'
    )

    target = serializers.ChoiceField(
        choices=languages_list,
        label='Target',
        help_text='Target field.'
    )

    def retrieve(self, validated_data: dict) -> dict:
        """ Try to get translations from db. """

        attrs = validated_data
        user = self.context['request'].user

        # Maybe Tranlation already exists?
        translation = HistoryTranslationsModel.objects.filter(
            text=attrs['message'],
            source=attrs['source'],
            target=attrs['target']
        )

        if translation:
            translation[0].history.add(user)
            if attrs.get('favorite', False):
                translation[0].favorite.add(user)

            return HistoryTranslationsModelSerializer(translation[0]).data
        else:
            return self.call_api(attrs, user)

    def call_api(self, attrs: dict, user: UserModel) -> dict:
        """ Call the Watson API. """

        payload = JSONRenderer().render({
            'text': [attrs['message']],
            'source': attrs['source'],
            'target': attrs['target']
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': env('WATSON_TOKEN')
        }
        response = requests.post(
            env('WATSON_API_TRANSLATE'),
            data=payload,
            headers=headers
        )
        data = response.json()

        if response.status_code != 200:
            raise NotFound()

        translation = HistoryTranslationsModel.objects.create(
            text=attrs['message'],
            source=attrs['source'],
            target=attrs['target'],
            translation=data['translations'][0]['translation'],
            word_count=data['word_count'],
            character_count=data['character_count']
        )
        translation.history.add(user)

        if attrs.get('favorite', False):
            translation.favorite.add(user)

        return HistoryTranslationsModelSerializer(translation).data
