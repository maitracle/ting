from rest_framework import serializers

from profiles.models import SelfDateProfile


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfDateProfile
        fields = (
            'user',
            'nickname',
            'gender',
            'scholarly_status',
            'campus_location',
        )


class ListProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    is_viewed = serializers.BooleanField()

    class Meta:
        model = SelfDateProfile
        fields = (
            'id',
            'image',
            'created_at',
            'updated_at',
            'nickname',
            'gender',
            'age',
            'height',
            'body_type',
            'religion',
            'tags',
            'image',
            'appearance',
            'personality',
            'hobby',
            'date_style',
            'ideal_type',
            'one_sentence',
            'is_viewed',
        )


class RetrieveProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = SelfDateProfile
        fields = (
            'id',
            'image',
            'created_at',
            'updated_at',
            'nickname',
            'gender',
            'age',
            'height',
            'body_type',
            'religion',
            'tags',
            'image',
            'appearance',
            'personality',
            'hobby',
            'date_style',
            'ideal_type',
            'one_sentence',
            'chat_link',
        )


class UpdateProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = SelfDateProfile
        fields = (
            'image',
            'age',
            'height',
            'body_type',
            'religion',
            'is_smoke',
            'tags',
            'image',
            'appearance',
            'personality',
            'hobby',
            'date_style',
            'ideal_type',
            'one_sentence',
            'chat_link',
        )
