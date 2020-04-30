from rest_framework import serializers

from coins.models import CoinHistory
from self_date.models import SelfDateProfile


class CreateCoinHistorySerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=SelfDateProfile.objects.all(), required=False)

    class Meta:
        model = CoinHistory
        fields = (
            'profile',
            'rest_coin',
            'reason',
            'message',
        )


class ListCoinHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = (
            'id',
            'profile',
            'rest_coin',
            'reason',
            'message',
            'created_at',
            'updated_at',
        )


class RetrieveCoinHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = (
            'id',
            'profile',
            'rest_coin',
            'reason',
            'message',)
