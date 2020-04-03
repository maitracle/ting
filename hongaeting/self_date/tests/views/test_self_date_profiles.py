import os
from unittest import skip

from PIL import Image
from assertpy import assert_that
from django.conf import settings
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from coins.models import CoinHistory
from common.constants import UNIVERSITY_CHOICES, COIN_CHANGE_REASON, REWORD_COUNT, COST_COUNT
from common.decorator import delete_media_root
from common.utils import reformat_datetime
from self_date.models import SelfDateProfile, SelfDateProfileRight
from users.models import Profile


class ProfileTestCase(APITestCase):
    def test_should_get_profile_list(self):
        # Given: user 1명과 profile이 주어진다.
        user = baker.make('users.User')
        profile_quantity = 10
        expected_profile_list = baker.make('self_date.SelfDateProfile', _quantity=profile_quantity)

        # When: user가 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/self-date-profiles/')

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
            'gender': 'MALE',
            'university': UNIVERSITY_CHOICES.HONGIK,
        }

        expected_profile = baker.make('self_date.SelfDateProfile', profile__gender=expected_profile_data['gender'],
                                      profile__university=expected_profile_data['university'])
        baker.make('self_date.SelfDateProfile', profile__gender=Profile.GENDER_CHOICES.FEMALE,
                   profile__university=UNIVERSITY_CHOICES.HONGIK)
        baker.make('self_date.SelfDateProfile', profile__gender=Profile.GENDER_CHOICES.MALE,
                   profile__university=UNIVERSITY_CHOICES.KYUNGHEE)
        baker.make('self_date.SelfDateProfile', profile__gender=Profile.GENDER_CHOICES.FEMALE,
                   profile__university=UNIVERSITY_CHOICES.KYUNGHEE)
        baker.make('self_date.SelfDateProfile', profile__gender=Profile.GENDER_CHOICES.MALE,
                   profile__university=UNIVERSITY_CHOICES.YONSEI)
        baker.make('self_date.SelfDateProfile', profile__gender=Profile.GENDER_CHOICES.FEMALE,
                   profile__university=UNIVERSITY_CHOICES.YONSEI)

        # When: user가 필터링 된 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/self-date-profiles/?'
                                   f'profile__gender={expected_profile_data["gender"]}'
                                   f'&profile__university={expected_profile_data["university"]}')

        # Then: 필터링 된 response가 온다.
        filtered_profile_quantity = 1
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(filtered_profile_quantity)

        expected_is_viewed_value = False
        for response in response.data:
            self._check_response_and_expected(response, expected_profile)
            assert_that(response['is_viewed']).is_equal_to(expected_is_viewed_value)

    @skip('coin history가 만들어질 때까지 테스트를 건너뛴다.')
    def test_is_viewed_in_list(self):
        # Given: user 하나와 여러 조합의 coin_history가 주어진다.
        user = baker.make('users.User')

        profile_quantity = 5
        profile_list = baker.make('self_date.SelfDateProfile', _quantity=profile_quantity)

        baker.make('coins.CoinHistory', user=user, reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
                   profile=profile_list[1])
        baker.make('coins.CoinHistory', user=user, reason=CoinHistory.CHANGE_REASON.SEND_MESSAGE,
                   profile=profile_list[2])
        baker.make('coins.CoinHistory', reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
                   profile=profile_list[3])
        baker.make('coins.CoinHistory', user=user, reason=CoinHistory.CHANGE_REASON.VIEW_PROFILE,
                   profile=profile_list[4])

        expected_is_viewed_list = [False, True, False, False, True]

        # When: user가 list api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/profiles/')

        # Then: user가 조회한 profile은 is_viewed값이 True이다.
        for response_profile, expected_is_viewed in zip(response.data, expected_is_viewed_list):
            assert_that(response_profile['is_viewed']).is_equal_to(expected_is_viewed)

    def test_should_get_retrieved_profile(self):
        # Given: coin이 충분한 request_self_date_profile과 target_self_date_profile이 주어진다.
        request_self_date_profile = baker.make('self_date.SelfDateProfile')
        target_self_date_profile = baker.make('self_date.SelfDateProfile')
        coin_history = baker.make(
            'coins.CoinHistory',
            profile=request_self_date_profile.profile,
            reason=COIN_CHANGE_REASON.CONFIRM_USER,
            rest_coin=REWORD_COUNT['CONFIRM_USER']
        )

        # When: request_self_date_profile의 user가 retrieve api를 호출한다.
        self.client.force_authenticate(user=request_self_date_profile.profile.user)
        response = self.client.get(f'/api/self-date-profiles/{target_self_date_profile.id}/')

        # Then: status code 200이 반환된다.
        #       profile 데이터가 반환된다.
        #       self_date_profile_right가 생성된다.
        #       coin 개수가 줄어든다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        self._check_response_and_expected(response.data, target_self_date_profile)

        self_date_profile_right = SelfDateProfileRight.objects.filter(
            buying_self_date_profile=request_self_date_profile,
            target_self_date_profile=target_self_date_profile,
            right_type=COIN_CHANGE_REASON.SELF_DATE_PROFILE_VIEW,
        )
        assert_that(self_date_profile_right.exists()).is_true()

        rest_coin = CoinHistory.objects.filter(profile=request_self_date_profile.profile).last().rest_coin
        assert_that(rest_coin).is_equal_to(
            coin_history.rest_coin - COST_COUNT[COIN_CHANGE_REASON.SELF_DATE_PROFILE_VIEW])

    def test_should_get_retrieved_profile_when_already_have_viewing_right(self):
        # Given: target에 대한 view 권한을 가진 request_self_date_profile이 주어진다.
        #        target_self_date_profile이 주어진다.
        request_self_date_profile = baker.make('self_date.SelfDateProfile')
        target_self_date_profile = baker.make('self_date.SelfDateProfile')

        baker.make('self_date.SelfDateProfileRight',
                   buying_self_date_profile=request_self_date_profile,
                   target_self_date_profile=target_self_date_profile,
                   right_type=COIN_CHANGE_REASON.SELF_DATE_PROFILE_VIEW)

        expected_rest_coin = 30
        baker.make('coins.CoinHistory', profile=request_self_date_profile.profile, rest_coin=expected_rest_coin)

        # When: request_self_date_profile의 user가 retrieve api를 호출한다.
        self.client.force_authenticate(user=request_self_date_profile.profile.user)
        response = self.client.get(f'/api/self-date-profiles/{target_self_date_profile.id}/')

        # Then: status code 200이 반환된다.
        #       profile이 반환된다.
        #       coin 개수가 감소하지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        self._check_response_and_expected(response.data, target_self_date_profile)
        rest_coin = CoinHistory.objects.filter(profile=request_self_date_profile.profile).last().rest_coin
        assert_that(rest_coin).is_equal_to(expected_rest_coin)

    def test_should_not_get_retrieved_profile_when_user_does_not_have_coin(self):
        # Given: target에 대한 view 권한을 가진 request_self_date_profile이 주어진다.
        #        target_self_date_profile이 주어진다.
        request_self_date_profile = baker.make('self_date.SelfDateProfile')
        target_self_date_profile = baker.make('self_date.SelfDateProfile')

        expected_rest_coin = 0
        baker.make('coins.CoinHistory', profile=request_self_date_profile.profile, rest_coin=expected_rest_coin)

        # When: request_self_date_profile의 user가 retrieve api를 호출한다.
        self.client.force_authenticate(user=request_self_date_profile.profile.user)
        response = self.client.get(f'/api/self-date-profiles/{target_self_date_profile.id}/')

        # Then: status code 403이 반환된다.
        #       코인 개수 부족 에러메시지가 반환된다.
        #       coin 개수가 감소하지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)
        assert_that(response.data['detail']).is_equal_to('코인 개수 부족으로 인한 permission denied')
        rest_coin = CoinHistory.objects.filter(profile=request_self_date_profile.profile).last().rest_coin
        assert_that(rest_coin).is_equal_to(expected_rest_coin)

    def _check_response_and_expected(self, dictionary, instance):
        assert_that(dictionary['image']).is_equal_to(instance.image)
        assert_that(dictionary['nickname']).is_equal_to(instance.nickname)
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
        assert_that(dictionary['created_at']).is_equal_to(reformat_datetime(instance.created_at))
        assert_that(dictionary['updated_at']).is_equal_to(reformat_datetime(instance.updated_at))

        assert_that(dictionary['profile']['id']).is_equal_to(instance.profile.id)
        assert_that(dictionary['profile']['user']).is_equal_to(instance.profile.user.id)
        assert_that(dictionary['profile']['gender']).is_equal_to(instance.profile.gender)
        assert_that(dictionary['profile']['born_year']).is_equal_to(instance.profile.born_year)
        assert_that(dictionary['profile']['university']).is_equal_to(instance.profile.university)
        assert_that(dictionary['profile']['campus_location']).is_equal_to(instance.profile.campus_location)
        assert_that(dictionary['profile']['scholarly_status']).is_equal_to(instance.profile.scholarly_status)
        assert_that(dictionary['profile']['created_at']).is_equal_to(reformat_datetime(instance.profile.created_at))
        assert_that(dictionary['profile']['updated_at']).is_equal_to(reformat_datetime(instance.profile.updated_at))

    def test_should_update_profile(self):
        # Given: user 1명과 그의 profile, 수정할 데이터가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('self_date.SelfDateProfile', profile__user=user, is_active=True)
        update_data = {
            'appearance': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
            파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자
            차카타파하'''
        }

        # When: user가 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/api/self-date-profiles/{profile.id}/', data=update_data)

        # Then: response가 정상적으로 오고, 수정할 데이터가 정상적으로 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['appearance']).is_equal_to(update_data['appearance'])

    @delete_media_root
    def test_should_update_image_at_profile(self):
        # Given: user 1명과 그의 profile, 수정할 image file이 주어진다.
        user = baker.make('users.User')
        profile = baker.make('self_date.SelfDateProfile', profile__user=user, is_active=True)

        try:
            image = Image.new('RGB', (100, 100))
            image.save('tmp_image.jpg')
            tmp_file = open('tmp_image.jpg', 'rb')
            update_data = {
                'image': tmp_file
            }

            # When: user가 update api를 호출한다.
            self.client.force_authenticate(user=user)
            response = self.client.patch(f'/api/self-date-profiles/{profile.id}/', data=update_data)

            # Then: profile의 image field가 반환된다.
            assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

            email_name, email_domain = user.email.split('@')
            expected_image_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/' \
                                 f'{settings.MEDIA_ROOT}/profiles/{email_name}%40{email_domain}/image.jpg'
            assert_that(response.data['image']).is_equal_to(expected_image_url)

        finally:
            # 임시로 만든 이미지 파일을 삭제한다.
            tmp_file.close()
            if os.path.exists('tmp_image.jpg'):
                os.remove('tmp_image.jpg')

    def test_should_fail_update_profile(self):
        # Given: user 1명과 다른 user의 profile, 수정할 데이터가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('self_date.SelfDateProfile', is_active=True)
        update_data = {
            'appearance': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
                    나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
                    파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자
                    차카타파하'''
        }

        # When: user가 update api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/api/self-date-profiles/{profile.id}/', data=update_data)

        # Then: 권한없음으로 update를 실패한다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)

        error_message = 'You do not have permission to perform this action.'
        error_code = 'permission_denied'
        assert_that(response.data['detail']).is_equal_to(error_message)
        assert_that(response.data['detail'].code).is_equal_to(error_code)

    def test_should_get_chat_link(self):
        # Given: user 1명과 메시지를 보낼 profile이 1개 주어진다. user의 rest_coin이 충분한 coin_history가 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('self_date.SelfDateProfile', chat_link='chatlink@test.com')
        coin_history = baker.make(
            'coins.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.CONFIRM_USER,
            rest_coin=SIGNUP_REWARD
        )

        # When: user가 send_message api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/self-date-profiles/{expected_profile.id}/chat-link/')

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
        expected_profile = baker.make('self_date.SelfDateProfile')
        coin_history = baker.make(
            'coins.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.SEND_MESSAGE,
            rest_coin=SIGNUP_REWARD - SEND_MESSAGE_COST,
            profile=expected_profile
        )

        # When: user가 send_message api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/self-date-profiles/{expected_profile.id}/chat-link/')

        # Then: 정상적으로 chat_link가 반환되고 user의 코인 개수는 줄어들지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['chat_link']).is_equal_to(expected_profile.chat_link)

        created_coin_history = CoinHistory.objects.filter(user=user).last()
        assert_that(created_coin_history.rest_coin).is_equal_to(coin_history.rest_coin)
        assert_that(created_coin_history.profile).is_equal_to(expected_profile)

    def test_should_not_get_chat_link_when_user_does_not_have_coin(self):
        # Given: user 1명과 메시지를 보낼 profile이 1개 주어진다. user의 rest_coin이 0인 coin_history가 주어진다.
        user = baker.make('users.User')
        expected_profile = baker.make('self_date.SelfDateProfile')
        coin_history = baker.make(
            'coins.CoinHistory',
            user=user,
            reason=CoinHistory.CHANGE_REASON.SEND_MESSAGE,
            rest_coin=0,
        )

        # When: user가 send_message api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/self-date-profiles/{expected_profile.id}/chat-link/')

        # Then: 403 에러가 반환되고 user의 코인 개수는 줄어들지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)

        created_coin_history = CoinHistory.objects.filter(user=user).last()
        assert_that(created_coin_history.rest_coin).is_equal_to(coin_history.rest_coin)

    def test_should_create_self_date_profile(self):
        # Given: user와 profile이 하나씩 주어지고 SelfDataProfile data가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('users.Profile', user=user)
        self_date_profile_data = {
            'profile': profile.id,
            'nickname': '테스트',
            'height': 70,
            'body_type': SelfDateProfile.BODY_TYPE_CHOICES.NORMAL,
            'religion': SelfDateProfile.RELIGION_CHOICES.NOTHING,
            'is_smoke': SelfDateProfile.IS_SMOKE_CHOICES.NO,
            'tags': '#1#2#3#4',
            'one_sentence': '한 문장 테스트',
            'appearance': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
            파하가나다라마바사아자차카타파하''',
            'personality': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하
            가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카
            타파하가나다라마바사아자차카타파하''',
            'hobby': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라
            마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하''',
            'date_style': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
            파하가나다라마바사아자차카타파하''',
            'ideal_type': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
            파하가나다라마바사아자차카타파하''',
            'chat_link': 'https://open.kakao.com/test/test'
        }

        # When: 주어진 user로 로그인 후 SelfDateProfile 생성 api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/self-date-profiles/', data=self_date_profile_data)

        # Then: status code 201과 생성된 SelfDateProfile이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        assert_that(response.data['profile']).is_equal_to(self_date_profile_data['profile'])
        assert_that(response.data['nickname']).is_equal_to(self_date_profile_data['nickname'])
        assert_that(response.data['height']).is_equal_to(self_date_profile_data['height'])
        assert_that(response.data['body_type']).is_equal_to(self_date_profile_data['body_type'])
        assert_that(response.data['religion']).is_equal_to(self_date_profile_data['religion'])
        assert_that(response.data['is_smoke']).is_equal_to(self_date_profile_data['is_smoke'])
        assert_that(response.data['tags']).is_equal_to(self_date_profile_data['tags'])
        assert_that(response.data['one_sentence']).is_equal_to(self_date_profile_data['one_sentence'])
        assert_that(response.data['appearance']).is_equal_to(self_date_profile_data['appearance'])
        assert_that(response.data['personality']).is_equal_to(self_date_profile_data['personality'])
        assert_that(response.data['hobby']).is_equal_to(self_date_profile_data['hobby'])
        assert_that(response.data['date_style']).is_equal_to(self_date_profile_data['date_style'])
        assert_that(response.data['ideal_type']).is_equal_to(self_date_profile_data['ideal_type'])
        assert_that(response.data['chat_link']).is_equal_to(self_date_profile_data['chat_link'])

    def test_should_not_create_self_date_profile_when_chat_link_is_invalid(self):
        # Given: user와 profile이 하나씩 생성되고 chat_link가 잘못된 SelfDateProfile data가 주어진다.
        user = baker.make('users.User')
        profile = baker.make('users.Profile', user=user)
        self_date_profile_data = {
            'profile': profile.id,
            'nickname': '테스트',
            'height': 70,
            'body_type': SelfDateProfile.BODY_TYPE_CHOICES.NORMAL,
            'religion': SelfDateProfile.RELIGION_CHOICES.NOTHING,
            'is_smoke': SelfDateProfile.IS_SMOKE_CHOICES.NO,
            'tags': '#1 #2 #3 #4',
            'one_sentence': '한 문장 테스트',
            'appearance': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
            파하가나다라마바사아자차카타파하''',
            'personality': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하
            가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카
            타파하가나다라마바사아자차카타파하''',
            'hobby': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라
            마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하''',
            'date_style': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
            파하가나다라마바사아자차카타파하''',
            'ideal_type': '''가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가
            나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타
            파하가나다라마바사아자차카타파하''',
            'chat_link': 'not URL'
        }

        # When: 생성된 user로 로그인 후 SelfDateProfile 생성 api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/self-date-profiles/', data=self_date_profile_data)

        # Then: status code 400이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

        chat_link_validation_error_msg = 'Not valid chat link'
        assert_that(chat_link_validation_error_msg in response.data['chat_link']).is_true()

        self_date_profiles = SelfDateProfile.objects.filter(profile=profile.id)
        assert_that(self_date_profiles).is_empty()
