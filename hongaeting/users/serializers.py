from rest_framework import serializers

from profiles.serializers import RetrieveProfileSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'university',
            'university_email',
        )


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=500)
    access = serializers.CharField(max_length=500)
    profile = RetrieveProfileSerializer()

    class Meta:
        fields = (
            'refresh',
            'access',
            'profile',
        )
