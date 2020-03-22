import tempfile

from PIL import Image
from assertpy import assert_that
from django.conf import settings
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.constants import UNIVERSITY_LIST, VIEW_PROFILE_COST, SIGNUP_REWARD, SEND_MESSAGE_COST
from common.decorator import delete_media_root
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

    def test_should_get_retrieved_profile(self):
        # Given: user 1명과 profile이 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('profiles.Profile')
        coin_history = baker.make(
            'self_date.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.SIGNUP,
            rest_coin=SIGNUP_REWARD
        )

        # When: user가 retrieve api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/{expected_profile.id}/')

        # Then: profile 데이터를 반환한다.
        #       coin 개수가 줄어든다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        self._check_response_and_expected(response.data, expected_profile)
        rest_coin = CoinHistory.objects.filter(user=user).last().rest_coin
        assert_that(rest_coin).is_equal_to(coin_history.rest_coin - VIEW_PROFILE_COST)

    def test_should_get_retrieved_profile_which_user_viewed(self):
        # Given: user 1명과 임의의 프로필 1개가 주어진다. 해당 프로필 조회 coin_history가 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('profiles.Profile')
        view_profile_coin_history = baker.make(
            'self_date.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
            rest_coin=28,
            profile=expected_profile,
        )

        # When: user가 retrieve api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/{expected_profile.id}/')

        # Then: profile이 반환된다. coin 개수가 감소하지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        self._check_response_and_expected(response.data, expected_profile)
        rest_coin = CoinHistory.objects.filter(user=user).last().rest_coin
        assert_that(rest_coin).is_equal_to(view_profile_coin_history.rest_coin)

    def test_should_not_get_retrieved_profile_when_user_does_not_have_coin(self):
        # Given: user 1명과 profile이 주어지고, coin이 남아있지 않은 coin_history가 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('profiles.Profile')
        final_coin_history = baker.make(
            'self_date.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
            rest_coin=0
        )

        # When: user가 retrieve api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/{expected_profile.id}/')

        # Then: 코인이 부족하여 403 forbidden 오류가 응답된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)
        rest_coin = CoinHistory.objects.filter(user=user).last().rest_coin
        assert_that(rest_coin).is_equal_to(final_coin_history.rest_coin)

    def _check_response_and_expected(self, dictionary, instance):
        assert_that(dictionary['image']).is_equal_to(instance.image)
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
        assert_that(dictionary['religion']).is_equal_to(instance.religion)
        assert_that(dictionary['date_style']).is_equal_to(instance.date_style)
        assert_that(dictionary['ideal_type']).is_equal_to(instance.ideal_type)
        assert_that(dictionary['one_sentence']).is_equal_to(instance.one_sentence)

    def test_should_update_profile(self):
        # Given: user 1명과 그의 profile, 수정할 데이터가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('profiles.Profile', user=user, is_active=True)
        update_data = {
            'appearance': """가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
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

    @delete_media_root
    def test_should_update_image_at_profile(self):
        # Given: user 1명과 그의 profile, 수정할 image file이 주어진다.
        user = baker.make('users.User')
        profile = baker.make('profiles.Profile', user=user, is_active=True)

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image = Image.new('RGB', (100, 100))
        image.save(tmp_file.name)
        update_data = {
            'image': tmp_file
        }

        # When: user가 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/api/profiles/{profile.id}/', data=update_data)

        # Then: profile의 image field가 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        email_name, email_domain = user.email.split('@')
        expected_image_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/' \
                             f'{settings.MEDIA_ROOT}/profiles/{email_name}%40{email_domain}/image.jpg'
        assert_that(response.data['image']).is_equal_to(expected_image_url)

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

    def test_should_get_chat_link(self):
        # Given: user 1명과 메시지를 보낼 profile이 1개 주어진다. user의 rest_coin이 충분한 coin_history가 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('profiles.Profile', chat_link="chatlink@test.com")
        coin_history = baker.make(
            'self_date.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.SIGNUP,
            rest_coin=SIGNUP_REWARD
        )

        # When: user가 send_message api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/{expected_profile.id}/chat-link/')

        # Then: 정상적으로 chat_link가 반환되고 user의 코인 개수가 비용만큼 줄어든다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['chat_link']).is_equal_to(expected_profile.chat_link)

        created_coin_history = CoinHistory.objects.filter(user=user).last()
        assert_that(created_coin_history.rest_coin).is_equal_to(coin_history.rest_coin - SEND_MESSAGE_COST)
        assert_that(created_coin_history.profile).is_equal_to(expected_profile)

    def test_should_get_chat_link_which_user_sent(self):
        # Given: user 1명과 메시지를 보낼 profile이 1개 주어진다.
        # user가 profile에게 메시지를 보냈적이 있음을 알리는 coin_history가 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('profiles.Profile')
        coin_history = baker.make(
            'self_date.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.SEND_MESSAGE,
            rest_coin=SIGNUP_REWARD - SEND_MESSAGE_COST,
            profile=expected_profile
        )

        # When: user가 send_message api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/{expected_profile.id}/chat-link/')

        # Then: 정상적으로 chat_link가 반환되고 user의 코인 개수는 줄어들지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['chat_link']).is_equal_to(expected_profile.chat_link)

        created_coin_history = CoinHistory.objects.filter(user=user).last()
        assert_that(created_coin_history.rest_coin).is_equal_to(coin_history.rest_coin)
        assert_that(created_coin_history.profile).is_equal_to(expected_profile)

    def test_should_not_get_chat_link_when_user_does_not_have_coin(self):
        # Given: user 1명과 메시지를 보낼 profile이 1개 주어진다. user의 rest_coin이 0인 coin_history가 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('profiles.Profile')
        coin_history = baker.make(
            'self_date.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.SEND_MESSAGE,
            rest_coin=0,
        )

        # When: user가 send_message api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/profiles/{expected_profile.id}/chat-link/')

        # Then: 403 에러가 반환되고 user의 코인 개수는 줄어들지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)

        created_coin_history = CoinHistory.objects.filter(user=user).last()
        assert_that(created_coin_history.rest_coin).is_equal_to(coin_history.rest_coin)
