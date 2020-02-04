from rest_framework import serializers

from self_date.models import CoinHistory


class CreateCoinHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = (
            'user',
            'rest_coin',
            'reason',
            'created_at',
            'updated_at',
        )
