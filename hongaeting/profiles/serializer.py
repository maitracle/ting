from rest_framework import serializers

from profiles.models import Profile


class ListProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'created_at',
            'updated_at',
            'nickname',
            'gender',
            'age',
            'height',
            'body_type',
            'tag',
            'image',
            'appearance',
            'personality',
            'hobby',
            'ideal_type',
            'last_tempting_word',
        )


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'tag',
            'image',
            'appearance',
            'personality',
            'hobby',
            'ideal_type',
            'last_tempting_word',
        )
