from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.constants import UNIVERSITY_CHOICE


class ProfileTestCase(APITestCase):
    def test_should_get_profile_list(self):
        # Given: user 1명과 그의 profile이 주어진다.
        user = baker.make('users.User')
        profile = baker.make('profiles.Profile', user=user)

        # When: user가 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/profiles/')

        # Then: response가 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data[0]['nickname']).is_equal_to(profile.nickname)

    def test_should_get_filtered_list(self):
        # Given: 로그인용 user 1명과 임의의 profile 1개가 주어진다.
        user_university = UNIVERSITY_CHOICE.HONGIK
        user = baker.make('users.User', university=user_university)
        profile = baker.make('profiles.Profile', user=user)

        # When: user가 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/?gender={profile.gender}&user__university={user.university}')

        # Then: response가 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data[0]['nickname']).is_equal_to(profile.nickname)

    def test_should_update_profile(self):
        # Given: user 1명과 그의 profile, 수정할 데이터가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('profiles.Profile', user=user, is_active=True)
        update_data = {
            "height": 180
        }

        # When: user가 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch('/api/profiles/1/', data=update_data)

        # Then: reponse가 정상적으로 오고, 수정할 데이터가 정상적으로 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['height']).is_equal_to(update_data["height"])

    def test_should_not_allow_same_nickname(self):
        # Given: 로그인용 user 1명과 임의의 profile 2개가 주어진다.
        exist_nickname = 'abc'
        user = baker.make('users.User')
        profile1 = baker.make('profiles.Profile', nickname=exist_nickname)
        profile2 = baker.make('profiles.Profile')
        update_data = {
            'nickname': exist_nickname
        }

        # When: profile2의 nickname을 exist_nickname으로 바꾸는 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch('/api/profiles/2/', data=update_data)

        # Then: 오류를 알리는 response 값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)
