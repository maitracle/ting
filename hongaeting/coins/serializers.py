from rest_framework import serializers

from coins.models import CoinHistory
from self_date.models import SelfDateProfile


class CreateCoinHistorySerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=SelfDateProfile.objects.all(), required=False)

    class Meta:
        model = CoinHistory
        fields = (
            'user',
            'rest_coin',
            'reason',
            'profile',
        )


class ListCoinHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = (
            'id',
            'user',
            'rest_coin',
            'reason',
            'profile',
            'created_at',
            'updated_at',
        )
