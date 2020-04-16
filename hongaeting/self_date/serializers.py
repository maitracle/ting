from rest_framework import serializers

from self_date.models import SelfDateLike
from users.serializers.profiles import ProfileSerializer
from .models import SelfDateProfile


class CreateSelfDateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfDateProfile
        fields = (
            'profile',
            'nickname',
            'height',
            'body_type',
            'religion',
            'is_smoke',
            'tags',
            'image',
            'one_sentence',
            'appearance',
            'personality',
            'hobby',
            'date_style',
            'ideal_type',
            'chat_link'
        )


class ListSelfDateProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    profile = ProfileSerializer()
    is_viewed = serializers.BooleanField()

    class Meta:
        model = SelfDateProfile
        fields = (
            'id',
            'profile',
            'nickname',
            'height',
            'body_type',
            'religion',
            'is_smoke',
            'tags',
            'image',
            'one_sentence',
            'appearance',
            'personality',
            'hobby',
            'date_style',
            'ideal_type',
            'is_viewed',
            'created_at',
            'updated_at',
        )


class RetrieveSelfDateProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    profile = ProfileSerializer()

    class Meta:
        model = SelfDateProfile
        fields = (
            'id',
            'profile',
            'nickname',
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
            'created_at',
            'updated_at',
        )


class UpdateSelfDateProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = SelfDateProfile
        fields = (
            'profile',
            'height',
            'body_type',
            'religion',
            'is_smoke',
            'tags',
            'image',
            'one_sentence',
            'appearance',
            'personality',
            'hobby',
            'date_style',
            'ideal_type',
            'chat_link',
            'created_at',
            'updated_at',
        )


class SelfDateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfDateLike
        fields = (
            'self_date_profile',
            'liked_self_date_profile',
            'created_at',
            'updated_at',
        )
