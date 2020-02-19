from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.constants import UNIVERSITY_LIST
from profiles.models import Profile


class ProfileTestCase(APITestCase):
    def _check_response_and_expected(self, dictionary, instance):
        assert_that(dictionary['nickname']).is_equal_to(instance.nickname)
        assert_that(dictionary['gender']).is_equal_to(instance.gender)
        assert_that(dictionary['age']).is_equal_to(instance.age)
        assert_that(dictionary['height']).is_equal_to(instance.height)
        assert_that(dictionary['body_type']).is_equal_to(instance.body_type)
        assert_that(dictionary['tag']).is_equal_to(instance.tag)
        assert_that(dictionary['image']).is_equal_to(instance.image)
        assert_that(dictionary['appearance']).is_equal_to(instance.appearance)
        assert_that(dictionary['personality']).is_equal_to(instance.personality)
        assert_that(dictionary['hobby']).is_equal_to(instance.hobby)
        assert_that(dictionary['ideal_type']).is_equal_to(instance.ideal_type)
        assert_that(dictionary['last_tempting_word']).is_equal_to(instance.last_tempting_word)

    def test_should_get_profile_list(self):
        # Given: user 1명과 그의 profile이 주어진다.
        profile_quantity = 10
        user = baker.make('users.User')
        expected_profile_list = baker.make('profiles.Profile', _quantity=profile_quantity)

        # When: user가 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/profiles/')

        # Then: response가 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(profile_quantity)
        for response_profile, expected_profile in zip(response.data, expected_profile_list):
            self._check_response_and_expected(response_profile, expected_profile)

    def test_should_get_filtered_list(self):
        # Given: 로그인용 user 1명과 임의의 profile 1개가 주어진다.
        user = baker.make('users.User')

        expected_profile_data = {
            "gender": "MALE",
            "university": "HONGIK"
        }

        expected_profile = baker.make('profiles.Profile', gender=expected_profile_data['gender'],
                                      user__university=expected_profile_data['university'])
        baker.make('profiles.Profile', gender=Profile.GENDER_CHOICES.FEMALE,
                   user__university=UNIVERSITY_LIST.HONGIK)
        baker.make('profiles.Profile', gender=Profile.GENDER_CHOICES.MALE,
                   user__university=UNIVERSITY_LIST.KYUNGHEE)
        baker.make('profiles.Profile', gender=Profile.GENDER_CHOICES.FEMALE,
                   user__university=UNIVERSITY_LIST.KYUNGHEE)
        baker.make('profiles.Profile', gender=Profile.GENDER_CHOICES.MALE,
                   user__university=UNIVERSITY_LIST.YONSEI)
        baker.make('profiles.Profile', gender=Profile.GENDER_CHOICES.FEMALE,
                   user__university=UNIVERSITY_LIST.YONSEI)

        # When: user가 필터링 된 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(
            f'/api/profiles/?gender={expected_profile_data["gender"]}&user__university={expected_profile_data["university"]}')

        # Then: 필터링 된 response가 온다.
        filtered_profile_quantity = 1
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(filtered_profile_quantity)
        for response in response.data:
            self._check_response_and_expected(response, expected_profile)

    def test_should_update_profile(self):
        # Given: user 1명과 그의 profile, 수정할 데이터가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('profiles.Profile', user=user, is_active=True)
        update_data = {
            "appearance": """가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
            파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자
            차카타파하"""
        }

        # When: user가 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/api/profiles/{profile.id}/', data=update_data)

        # Then: response가 정상적으로 오고, 수정할 데이터가 정상적으로 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['appearance']).is_equal_to(update_data['appearance'])
