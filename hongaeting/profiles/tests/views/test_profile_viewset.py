from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.constants import UNIVERSITY_CHOICE
from profiles.models import Profile


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
        user = baker.make('users.User')

        expected_profile_data = {
            "gender": "MALE",
            "university": "HONGIK"
        }
        expected_profile_quantity = 1
        expected_profile = baker.make('profiles.Profile', gender=expected_profile_data['gender'],
                                      user__university=expected_profile_data['university'])
        profile1 = baker.make('profiles.Profile', gender=Profile.GENDER_CHOICE.FEMALE,
                              user__university=UNIVERSITY_CHOICE.HONGIK)
        profile2 = baker.make('profiles.Profile', gender=Profile.GENDER_CHOICE.MALE,
                              user__university=UNIVERSITY_CHOICE.KYUNGHEE)
        profile3 = baker.make('profiles.Profile', gender=Profile.GENDER_CHOICE.FEMALE,
                              user__university=UNIVERSITY_CHOICE.KYUNGHEE)
        profile4 = baker.make('profiles.Profile', gender=Profile.GENDER_CHOICE.MALE,
                              user__university=UNIVERSITY_CHOICE.YONSEI)
        profile5 = baker.make('profiles.Profile', gender=Profile.GENDER_CHOICE.FEMALE,
                              user__university=UNIVERSITY_CHOICE.YONSEI)

        # When: user가 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/?gender={expected_profile_data["gender"]}&user__university={expected_profile_data["university"]}')

        # Then: response가 정상적으로 온다. 길이,
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(expected_profile_quantity)
        for i in range(expected_profile_quantity):
            assert_that(response.data[i]['nickname']).is_equal_to(expected_profile.nickname)
            assert_that(response.data[i]['gender']).is_equal_to(expected_profile.gender)
            assert_that(response.data[i]['age']).is_equal_to(expected_profile.age)
            assert_that(response.data[i]['height']).is_equal_to(expected_profile.height)
            assert_that(response.data[i]['body_type']).is_equal_to(expected_profile.body_type)
            assert_that(response.data[i]['tag']).is_equal_to(expected_profile.tag)
            assert_that(response.data[i]['image']).is_equal_to(expected_profile.image)
            assert_that(response.data[i]['appearance']).is_equal_to(expected_profile.appearance)
            assert_that(response.data[i]['personality']).is_equal_to(expected_profile.personality)
            assert_that(response.data[i]['hobby']).is_equal_to(expected_profile.hobby)
            assert_that(response.data[i]['ideal_type']).is_equal_to(expected_profile.ideal_type)
            assert_that(response.data[i]['last_tempting_word']).is_equal_to(expected_profile.last_tempting_word)

    def test_should_update_profile(self):
        # Given: user 1명과 그의 profile, 수정할 데이터가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('profiles.Profile', user=user, is_active=True)
        update_data = {
            "appearance": "가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하"
        }

        # When: user가 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/api/profiles/{profile.id}/', data=update_data)

        # Then: response가 정상적으로 오고, 수정할 데이터가 정상적으로 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['appearance']).is_equal_to(update_data['appearance'])
