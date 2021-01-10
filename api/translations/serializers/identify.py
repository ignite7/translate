""" Identify serializers. """

# Django REST framework
from rest_framework.exceptions import NotFound

# Serializers
from api.translations.serializers.commons import (
    HistoryModelSerializer,
    HistoryIdentifyModelSerializer
)

# Models
from api.histories.models import HistoryIdentifyModel
from api.users.models.users import UserModel

# Utilities
import requests
import environ

# Environ
env = environ.Env()
environ.Env.read_env()


class IdentifySerializer(HistoryModelSerializer):
    """ Indntify serializers class. """

    def retrieve(self, validated_data: dict) -> dict:
        """ Try to get translations from db. """

        attrs = validated_data
        user = self.context['request'].user

        # Maybe Tranlation already exists?
        identify = HistoryIdentifyModel.objects.filter(text=attrs['message'])

        if identify:
            identify[0].history.add(user)
            if attrs.get('favorite', False):
                identify[0].favorite.add(user)

            return HistoryIdentifyModelSerializer(identify[0]).data
        else:
            return self.call_api(attrs, user)

    def call_api(self, attrs: dict, user: UserModel) -> dict:
        """ Call the Watson API. """

        payload = attrs['message']
        headers = {
            'Content-Type': 'text/plain',
            'Authorization': env('WATSON_TOKEN')
        }
        response = requests.post(
            env('WATSON_API_IDENTIFY'),
            data=payload,
            headers=headers
        )
        data = response.json()

        if response.status_code != 200:
            raise NotFound()

        identify = HistoryIdentifyModel.objects.create(
            text=attrs['message'],
            identify_languages=data
        )
        identify.history.add(user)

        if attrs.get('favorite', False):
            identify.favorite.add(user)

        return HistoryIdentifyModelSerializer(identify).data
