from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'nickname',
            'gender',
            'age',
            'height',
            'body_type',
            'tag',
            'image',
        )
