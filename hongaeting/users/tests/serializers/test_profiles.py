from assertpy import assert_that
from model_bakery import baker
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from common.constants import UNIVERSITY_CHOICES, MAP_UNIVERSITY_WITH_CAMPUS
from users.models import Profile
from users.serializers.profiles import ProfileSerializer


class ProfileSerializerTestCase(APITestCase):

    def test_validate(self):
        # Given: user가 주어지고, campus_location 필드가 잘못된 profile에 관한 데이터가 주어진다.
        user = baker.make('users.User')
        profile_data = {
            'user' : user.id,
            'nickname': 'nickname',
            'gender': Profile.GENDER_CHOICES.MALE,
            'born_year': 1999,
            'university': UNIVERSITY_CHOICES.HONGIK,
            'campus_location': MAP_UNIVERSITY_WITH_CAMPUS[UNIVERSITY_CHOICES.YONSEI][0],
            'scholarly_status': Profile.SCHOLARLY_STATUS_CHOICES.ATTENDING,
        }

        # When: 주어진 profile_data로 ProfileSerializer 인스턴스를 생성하고, validate 메소드를 실행한다.
        profile_serializer = ProfileSerializer(data=profile_data)
        try:
            profile_serializer.validate(profile_serializer.initial_data)

        # Then: ValidationError가 발생한다.
        except Exception as e:
            assert_that(e).is_instance_of(ValidationError)
            assert_that(e.args[0]).is_equal_to('Wrong campus location.')
