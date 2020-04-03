from rest_framework import serializers

from common.constants import MAP_UNIVERSITY_WITH_CAMPUS
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'nickname',
            'gender',
            'born_year',
            'university',
            'campus_location',
            'scholarly_status',
            'created_at',
            'updated_at',
        )

    def validate(self, attrs):
        if 'campus_location' in attrs:
            if not attrs['campus_location'] in MAP_UNIVERSITY_WITH_CAMPUS[attrs['university']]:
                raise serializers.ValidationError('Wrong campus location.')

        return attrs
