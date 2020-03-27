from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'gender',
            'birthday',
            'university',
            'campus_location',
            'scholarly_status',
            'created_at',
            'updated_at',
        )
