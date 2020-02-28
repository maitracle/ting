from rest_framework import serializers

from profiles.serializers import MyProfileSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'university',
        )


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    profile = MyProfileSerializer()

    class Meta:
        fields = (
            'refresh',
            'access',
            'profile',
        )
