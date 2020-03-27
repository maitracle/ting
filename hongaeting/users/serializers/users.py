from rest_framework import serializers

from self_date.serializer import ListCoinHistorySerializer
from users.models import User
from users.serializers.profiles import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    student_id_card_image = serializers.ImageField(use_url=True, required=False)
    is_confirmed_student = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'student_id_card_image',
            'is_confirmed_student',
        )


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
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
    profile = ProfileSerializer()
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
    profile = ProfileSerializer()
    coin_history = ListCoinHistorySerializer(many=True)

    class Meta:
        fields = (
            'user',
            'profile',
            'coin_history',
        )
