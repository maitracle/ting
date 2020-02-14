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
        assert_that(response.data[0]['gender']).is_equal_to(profile.gender)
        assert_that(response.data[0]['age']).is_equal_to(profile.age)
        assert_that(response.data[0]['height']).is_equal_to(profile.height)
        assert_that(response.data[0]['body_type']).is_equal_to(profile.body_type)
        assert_that(response.data[0]['tag']).is_equal_to(profile.tag)
        assert_that(response.data[0]['image']).is_equal_to(profile.image)
        assert_that(response.data[0]['appearance']).is_equal_to(profile.appearance)
        assert_that(response.data[0]['personality']).is_equal_to(profile.personality)
        assert_that(response.data[0]['hobby']).is_equal_to(profile.hobby)
        assert_that(response.data[0]['ideal_type']).is_equal_to(profile.ideal_type)
        assert_that(response.data[0]['last_tempting_word']).is_equal_to(profile.last_tempting_word)


    def test_should_update_profile(self):
        # Given: user 1명과 그의 profile, 수정할 데이터가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('profiles.Profile', user=user, is_active=True)
        update_data = {
            "appearance": "가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하"
        }

        # When: user가 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch('/api/profiles/1/', data=update_data)

        # Then: response가 정상적으로 오고, 수정할 데이터가 정상적으로 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['appearance']).is_equal_to(update_data['appearance'])
