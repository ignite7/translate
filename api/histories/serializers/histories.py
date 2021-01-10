""" History serializers. """

# Django REST framework
from rest_framework import serializers

# Models
from api.histories.models import (
    HistoryTranslationsModel,
    HistoryIdentifyModel
)

# Serializers
from api.histories.serializers.commons import (
    HistoryTranlationSerializer,
    HistoryIdenfySerializer
)


class HistorySerializer(serializers.Serializer):
    """ Delete history serializer class. """

    def retrieve(self) -> dict:
        """ Join histories identifies and translations. """

        user = self.context['request'].user
        translations = HistoryTranslationsModel.objects.filter(history=user)
        identifies = HistoryIdentifyModel.objects.filter(history=user)

        return {
            'translations': HistoryTranlationSerializer(
                translations, many=True
            ).data,
            'identifies': HistoryIdenfySerializer(
                identifies, many=True
            ).data
        }

    def delete_all(self) -> dict:
        """ Delete user histories """

        user = self.context['request'].user
        translations = HistoryTranslationsModel.objects.filter(history=user)
        identifies = HistoryIdentifyModel.objects.filter(history=user)

        for translation in translations:
            translation.history.clear()
            translation.favorite.clear()

        for identify in identifies:
            identify.history.clear()
            identify.favorite.clear()

        return {'message': 'Histories has been deleted successfully.'}

    def delete(self) -> dict:
        """ Delete specific user history. """

        user = self.context['request'].user
        uuid = self.context['uuid']
        translations = HistoryTranslationsModel.objects.filter(pk=uuid)
        identifies = HistoryIdentifyModel.objects.filter(pk=uuid)

        for translation in translations:
            translation.history.remove(user)
            translation.favorite.remove(user)

        for identify in identifies:
            identify.history.remove(user)
            identify.favorite.remove(user)

        return {
            'message': f'The history <{uuid}> has been deleted successfully.'
        }
