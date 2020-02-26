from rest_framework import serializers

from profiles.serializers import LogInProfileSerializer
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
    access = serializers.CharField()
    refresh = serializers.CharField()
    profile = LogInProfileSerializer()
    university = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'refresh',
            'access',
            'profile',
            'university',
        )

    def get_university(self, obj):
        return obj['profile'].user.university
