""" Favorites serializers. """

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


class FavoriteSerializer(serializers.Serializer):
    """ Get or delete favorite serializer class. """

    def retrieve(self) -> dict:
        """ Join favorites identifies and translations. """

        user = self.context['request'].user
        translations = HistoryTranslationsModel.objects.filter(favorite=user)
        identifies = HistoryIdentifyModel.objects.filter(favorite=user)

        return {
            'translations': HistoryTranlationSerializer(
                translations, many=True
            ).data,
            'identifies': HistoryIdenfySerializer(
                identifies, many=True
            ).data
        }

    def delete_all(self) -> dict:
        """ Delete user favorites """

        user = self.context['request'].user
        translations = HistoryTranslationsModel.objects.filter(favorite=user)
        identifies = HistoryIdentifyModel.objects.filter(favorite=user)

        for translation in translations:
            translation.favorite.clear()

        for identify in identifies:
            identify.favorite.clear()

        return {'message': 'Favorites has been deleted successfully.'}

    def delete(self) -> dict:
        """ Delete specific user history. """

        user = self.context['request'].user
        uuid = self.context['uuid']
        translations = HistoryTranslationsModel.objects.filter(pk=uuid)
        identifies = HistoryIdentifyModel.objects.filter(pk=uuid)

        for translation in translations:
            translation.favorite.remove(user)

        for identify in identifies:
            identify.favorite.remove(user)

        return {
            'message': f'The favorite <{uuid}> has been deleted successfully.'
        }

    def create(self):
        """ Create new favorite item. """

        user = self.context['request'].user
        uuid = self.context['uuid']
        translations = HistoryTranslationsModel.objects.filter(pk=uuid)
        identifies = HistoryIdentifyModel.objects.filter(pk=uuid)

        for translation in translations:
            translation.favorite.add(user)

        for identify in identifies:
            identify.favorite.add(user)

        return {'message': 'Favorite item created successfully.'}
