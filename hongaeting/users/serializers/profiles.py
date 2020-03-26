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
            'scholarly_status',
            'campus_location',
            'created_at',
            'updated_at',
        )