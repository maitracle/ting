from assertpy import assert_that
from model_bakery import baker
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from common.constants import UNIVERSITY_CHOICES, MAP_UNIVERSITY_WITH_CAMPUS
from users.models import Profile
from users.serializers.profiles import CreateOrUpdateProfileSerializer


class CreateOrUpdateProfileSerializerTestCase(APITestCase):

    def test_validate_when_valid(self):
        # Given: user가 주어지고, 유효한 profile_serializer가 주어진다.
        user = baker.make('users.User')
        profile_data = {
            'user': user.id,
            'nickname': 'nickname',
            'gender': Profile.GENDER_CHOICES.MALE,
            'born_year': 1999,
            'university': UNIVERSITY_CHOICES.HONGIK,
            'campus_location': MAP_UNIVERSITY_WITH_CAMPUS[UNIVERSITY_CHOICES.HONGIK][0],
            'scholarly_status': Profile.SCHOLARLY_STATUS_CHOICES.ATTENDING,
        }
        profile_serializer = CreateOrUpdateProfileSerializer(data=profile_data)

        # When: validate 메소드를 실행한다.
        attrs = profile_serializer.validate(profile_serializer.initial_data)

        # Then: validate 메소드의 리턴값과 profile_data가 일치한다.
        assert_that(attrs['user']).is_equal_to(profile_data['user'])
        assert_that(attrs['nickname']).is_equal_to(profile_data['nickname'])
        assert_that(attrs['gender']).is_equal_to(profile_data['gender'])
        assert_that(attrs['born_year']).is_equal_to(profile_data['born_year'])
        assert_that(attrs['university']).is_equal_to(profile_data['university'])
        assert_that(attrs['campus_location']).is_equal_to(profile_data['campus_location'])
        assert_that(attrs['scholarly_status']).is_equal_to(profile_data['scholarly_status'])


    def test_validate_when_invalid(self):
        # Given: user가 주어지고, campus_location 필드가 잘못된 profile_serializer가 주어진다.
        user = baker.make('users.User')
        profile_data = {
            'user': user.id,
            'nickname': 'nickname',
            'gender': Profile.GENDER_CHOICES.MALE,
            'born_year': 1999,
            'university': UNIVERSITY_CHOICES.HONGIK,
            'campus_location': MAP_UNIVERSITY_WITH_CAMPUS[UNIVERSITY_CHOICES.YONSEI][0],
            'scholarly_status': Profile.SCHOLARLY_STATUS_CHOICES.ATTENDING,
        }
        profile_serializer = CreateOrUpdateProfileSerializer(data=profile_data)

        # When: validate 메소드를 실행한다.
        try:
            profile_serializer.validate(profile_serializer.initial_data)

        # Then: ValidationError가 발생한다.
        except ValidationError as e:
            assert_that(e.args[0]).is_equal_to('Wrong campus location.')
        else:
            self.fail()
