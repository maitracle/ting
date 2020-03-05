from rest_framework import serializers

from profiles.serializers import RetrieveProfileSerializer
from self_date.serializer import ListCoinHistorySerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    is_confirmed_student = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'university',
            'is_confirmed_student',
        )


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'university',
            'user_code',
            'is_confirmed_student',
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
