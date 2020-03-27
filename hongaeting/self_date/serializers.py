from rest_framework import serializers

from self_date.models import Like
from users.serializers.profiles import ProfileSerializer
from .models import SelfDateProfile


class CreateSelfDateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfDateProfile
        fields = (
            'user',
            'nickname',
            'gender',
            'scholarly_status',
            'campus_location',
        )


class ListSelfDateProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    profile = ProfileSerializer()
    is_viewed = serializers.BooleanField()

    class Meta:
        model = SelfDateProfile
        fields = (
            'id',
            'image',
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
            'is_viewed',
            'profile',
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
            'image',
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
            'profile',
            'created_at',
            'updated_at',
        )


class UpdateSelfDateProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = SelfDateProfile
        fields = (
            'image',
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
            'profile',
            'created_at',
            'updated_at',
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'user',
            'liked_user',
            'created_at',
            'updated_at',
        )
