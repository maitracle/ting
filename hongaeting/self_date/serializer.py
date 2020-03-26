from rest_framework import serializers
from profiles.models import SelfDateProfile
from self_date.models import CoinHistory, Like


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


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'user',
            'liked_user',
            'created_at',
            'updated_at',
        )
