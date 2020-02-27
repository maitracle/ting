from rest_framework import serializers

from profiles.models import Profile


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'user',
            'nickname',
            'gender',
            'scholarly_status',
            'campus_location',
        )


class ListProfileSerializer(serializers.ModelSerializer):
    is_viewed = serializers.BooleanField()

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
            'tags',
            'image',
            'appearance',
            'personality',
            'hobby',
            'ideal_type',
            'one_sentence',
            'is_viewed',
        )


class RetrieveProfileSerializer(serializers.ModelSerializer):
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
            'tags',
            'image',
            'appearance',
            'personality',
            'hobby',
            'ideal_type',
            'one_sentence',
        )


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'tags',
            'image',
            'appearance',
            'personality',
            'hobby',
            'ideal_type',
            'one_sentence',
        )


class MyProfileSerializer(serializers.ModelSerializer):
    university = serializers.SerializerMethodField()

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
            'tags',
            'image',
            'appearance',
            'personality',
            'hobby',
            'ideal_type',
            'one_sentence',
            'chat_link',
            'university',
        )

    def get_university(self, obj):
        return obj.user.university
