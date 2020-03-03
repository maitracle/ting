from rest_framework import serializers

from profiles.serializers import RetrieveProfileSerializer
from self_date.serializer import ListCoinHistorySerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'university',
        )


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'university',
            'user_code',
        )


class UserCheckUnivSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'university_email',
        )


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = RetrieveUserSerializer()
    profile = RetrieveProfileSerializer()
    coin_history = ListCoinHistorySerializer(many=True)

    class Meta:
        fields = (
            'refresh',
            'access',
            'user',
            'profile',
            'coin_history',
        )


class MySerializer(serializers.Serializer):
    user = RetrieveUserSerializer()
    profile = RetrieveProfileSerializer()
    coin_history = ListCoinHistorySerializer(many=True)

    class Meta:
        fields = (
            'user',
            'profile',
            'coin_history',
        )
