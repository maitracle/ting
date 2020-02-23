from rest_framework import serializers

from self_date.models import CoinHistory, Like


class ListCoinHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = (
            'user',
            'rest_coin',
            'reason',
            'profile',
            'created_at',
            'updated_at',
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'user',
            'liked_user',
            'created_at',
            'updated_at',
        )
