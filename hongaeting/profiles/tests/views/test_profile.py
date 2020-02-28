from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.constants import UNIVERSITY_LIST
from profiles.models import Profile
from self_date.models import CoinHistory


class ProfileTestCase(APITestCase):

    def test_should_get_profile_list(self):
        # Given: user 1명과 profile이 주어진다.
        user = baker.make('users.User')
        profile_quantity = 10
        expected_profile_list = baker.make('profiles.Profile', _quantity=profile_quantity)

        # When: user가 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/profiles/')

        # Then: response가 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(profile_quantity)

        expected_is_viewed_value = False
        for response_profile, expected_profile in zip(response.data, expected_profile_list):
            self._check_response_and_expected(response_profile, expected_profile)
            assert_that(response_profile['is_viewed']).is_equal_to(expected_is_viewed_value)

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

        expected_is_viewed_value = False
        for response in response.data:
            self._check_response_and_expected(response, expected_profile)
            assert_that(response['is_viewed']).is_equal_to(expected_is_viewed_value)

    def test_is_viewed_in_list(self):
        # Given: user 하나와 여러 조합의 coin_history가 주어진다.
        user = baker.make('users.User')

        profile_quantity = 5
        profile_list = baker.make('profiles.Profile', _quantity=profile_quantity)

        baker.make('self_date.CoinHistory', user=user, reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
                   profile=profile_list[1])
        baker.make('self_date.CoinHistory', user=user, reason=CoinHistory.CHANGE_REASON.SEND_MESSAGE,
                   profile=profile_list[2])
        baker.make('self_date.CoinHistory', reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
                   profile=profile_list[3])
        baker.make('self_date.CoinHistory', user=user, reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
                   profile=profile_list[4])

        expected_is_viewed_list = [False, True, False, False, True]

        # When: user가 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/profiles/')

        # Then: user가 조회한 profile은 is_viewed값이 True이다.
        for response_profile, expected_is_viewed in zip(response.data, expected_is_viewed_list):
            assert_that(response_profile['is_viewed']).is_equal_to(expected_is_viewed)

    def test_should_get_profile_retrieve(self):
        # Given: user 1명과 profile이 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('profiles.Profile')

        # When: user가 retrieve api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/{expected_profile.id}/')

        # Then: response가 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        self._check_response_and_expected(response.data, expected_profile)

    def _check_response_and_expected(self, dictionary, instance):
        assert_that(dictionary['nickname']).is_equal_to(instance.nickname)
        assert_that(dictionary['gender']).is_equal_to(instance.gender)
        assert_that(dictionary['age']).is_equal_to(instance.age)
        assert_that(dictionary['height']).is_equal_to(instance.height)
        assert_that(dictionary['body_type']).is_equal_to(instance.body_type)
        assert_that(dictionary['tags']).is_equal_to(instance.tags)
        assert_that(dictionary['image']).is_equal_to(instance.image)
        assert_that(dictionary['appearance']).is_equal_to(instance.appearance)
        assert_that(dictionary['personality']).is_equal_to(instance.personality)
        assert_that(dictionary['hobby']).is_equal_to(instance.hobby)
        assert_that(dictionary['ideal_type']).is_equal_to(instance.ideal_type)
        assert_that(dictionary['one_sentence']).is_equal_to(instance.one_sentence)

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

    def test_should_fail_update_profile(self):
        # Given: user 1명과 다른 user의 profile, 수정할 데이터가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('profiles.Profile', is_active=True)
        update_data = {
            "appearance": """가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
                    나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
                    파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자
                    차카타파하"""
        }

        # When: user가 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/api/profiles/{profile.id}/', data=update_data)

        # Then: 권한없음으로 update를 실패한다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)

        error_message = 'You do not have permission to perform this action.'
        error_code = 'permission_denied'
        assert_that(response.data['detail']).is_equal_to(error_message)
        assert_that(response.data['detail'].code).is_equal_to(error_code)

    def test_should_get_my_profile(self):
        # Given: user와 profile이 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('profiles.Profile', user=user)

        # When: user가 my profile api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/my/')

        # Then: 자신의 profile이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        assert_that(response.data['university']).is_equal_to(user.university)

        assert_that(response.data['nickname']).is_equal_to(expected_profile.nickname)
        assert_that(response.data['gender']).is_equal_to(expected_profile.gender)
        assert_that(response.data['age']).is_equal_to(expected_profile.age)
        assert_that(response.data['height']).is_equal_to(expected_profile.height)
        assert_that(response.data['body_type']).is_equal_to(expected_profile.body_type)
        assert_that(response.data['tags']).is_equal_to(expected_profile.tags)
        assert_that(response.data['image']).is_equal_to(expected_profile.image)
        assert_that(response.data['appearance']).is_equal_to(expected_profile.appearance)
        assert_that(response.data['personality']).is_equal_to(expected_profile.personality)
        assert_that(response.data['hobby']).is_equal_to(expected_profile.hobby)
        assert_that(response.data['date_style']).is_equal_to(expected_profile.date_style)
        assert_that(response.data['ideal_type']).is_equal_to(expected_profile.ideal_type)
        assert_that(response.data['one_sentence']).is_equal_to(expected_profile.one_sentence)
        assert_that(response.data['chat_link']).is_equal_to(expected_profile.chat_link)
