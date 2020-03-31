import json

from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.constants import UNIVERSITY_CHOICES, MAP_UNIVERSITY_WITH_CAMPUS
from common.utils import reformat_datetime
from users.models import Profile


class ProfileViewSetTestCase(APITestCase):

    def test_create_profile(self):
        # Given: 만들어질 profile에 관한 데이터가 주어진다.
        user = baker.make('users.User')
        profile_data = {
            'nickname': 'nickname',
            'gender': Profile.GENDER_CHOICES.MALE,
            'born_year': 1999,
            'university': UNIVERSITY_CHOICES.HONGIK,
            'campus_location': MAP_UNIVERSITY_WITH_CAMPUS[UNIVERSITY_CHOICES.HONGIK][0],
            'scholarly_status': Profile.SCHOLARLY_STATUS_CHOICES.ATTENDING,
        }

        # When: user create api를 호출하여 회원가입을 한다.
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/profiles/', data=json.dumps(profile_data), content_type='application/json')

        # Then: 만들어진 Profile이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        expected_profile = Profile.objects.get(nickname=profile_data['nickname'])

        assert_that(response.data['id']).is_equal_to(expected_profile.id)
        assert_that(response.data['nickname']).is_equal_to(profile_data['nickname'])
        assert_that(response.data['gender']).is_equal_to(profile_data['gender'])
        assert_that(response.data['born_year']).is_equal_to(profile_data['born_year'])
        assert_that(response.data['university']).is_equal_to(profile_data['university'])
        assert_that(response.data['campus_location']).is_equal_to(profile_data['campus_location'])
        assert_that(response.data['scholarly_status']).is_equal_to(profile_data['scholarly_status'])
        assert_that(response.data['created_at']).is_equal_to(reformat_datetime(expected_profile.created_at))
        assert_that(response.data['updated_at']).is_equal_to(reformat_datetime(expected_profile.updated_at))

    def test_update_profile(self):
        # Given: 수정될 profile과 바뀔 data가 주어진다.
        profile = baker.make('users.Profile', scholarly_status=Profile.SCHOLARLY_STATUS_CHOICES.ATTENDING)
        updated_data = {
            'scholarly_status': Profile.SCHOLARLY_STATUS_CHOICES.TAKING_OFF,
        }

        # When: profile update api를 호출하여 회원가입을 한다.
        self.client.force_authenticate(user=profile.user)
        response = self.client.patch(f'/api/profiles/{profile.id}/', data=updated_data)

        # Then: 수정된 Profile이 반환된다.
        #       수정한 field와 updated_at field가 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        updated_profile = Profile.objects.get(id=profile.id)

        assert_that(response.data['id']).is_equal_to(profile.id)
        assert_that(response.data['nickname']).is_equal_to(profile.nickname)
        assert_that(response.data['gender']).is_equal_to(profile.gender)
        assert_that(response.data['born_year']).is_equal_to(profile.born_year)
        assert_that(response.data['university']).is_equal_to(profile.university)
        assert_that(response.data['campus_location']).is_equal_to(profile.campus_location)
        assert_that(response.data['created_at']).is_equal_to(reformat_datetime(profile.created_at))

        assert_that(response.data['scholarly_status']).is_equal_to(updated_profile.scholarly_status)
        assert_that(response.data['updated_at']).is_equal_to(reformat_datetime(updated_profile.updated_at))

    def test_should_fail_update_profile(self):
        # Given: 수정될 profile과 바뀔 data가 주어진다.
        another_user = baker.make('users.User')
        profile = baker.make('users.Profile', scholarly_status=Profile.SCHOLARLY_STATUS_CHOICES.ATTENDING)
        updated_data = {
            'scholarly_status': Profile.SCHOLARLY_STATUS_CHOICES.TAKING_OFF,
        }

        # When: profile update api를 호출하여 회원가입을 한다.
        self.client.force_authenticate(user=another_user)
        response = self.client.patch(f'/api/profiles/{profile.id}/', data=updated_data)

        # Then: 수정된 Profile이 반환된다.
        #       수정한 field와 updated_at field가 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)

        assert_that(response.data.detail).is_equal_to('You do not have permission to perform this action.')

        # updated_profile = Profile.objects.get(id=profile.id)

        assert_that(response.data['id']).is_equal_to(profile.id)
        assert_that(response.data['nickname']).is_equal_to(profile.nickname)
        assert_that(response.data['gender']).is_equal_to(profile.gender)
        assert_that(response.data['born_year']).is_equal_to(profile.born_year)
        assert_that(response.data['university']).is_equal_to(profile.university)
        assert_that(response.data['campus_location']).is_equal_to(profile.campus_location)
        assert_that(response.data['created_at']).is_equal_to(reformat_datetime(profile.created_at))

        assert_that(response.data['scholarly_status']).is_equal_to(profile.scholarly_status)
        assert_that(response.data['updated_at']).is_equal_to(reformat_datetime(profile.updated_at))
