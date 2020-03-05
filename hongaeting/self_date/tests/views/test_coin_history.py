from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.constants import SIGNUP_REWARD, SEND_MESSAGE_COST
from common.utils import reformat_datetime
from self_date.models import CoinHistory


class CoinHistoryTestCase(APITestCase):
    def test_should_get_list(self):
        # Given: user 1명이 생성되고 그 유저의 coin-history가 생성된다.
        user = baker.make('users.User')
        coin_history_quantity = 3
        expected_coin_histories = baker.make('self_date.CoinHistory', user=user, _quantity=coin_history_quantity)

        # When: user가 coin_history_list api 호출
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/coin-histories/')

        # Then: response값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(coin_history_quantity)

        for responded_coin_history, expected_coin_history in zip(response.data, expected_coin_histories):
            assert_that(responded_coin_history['user']).is_equal_to(user.id)
            assert_that(responded_coin_history['rest_coin']).is_equal_to(expected_coin_history.rest_coin)
            assert_that(responded_coin_history['reason']).is_equal_to(expected_coin_history.reason)
            assert_that(responded_coin_history['profile']).is_equal_to(expected_coin_history.profile)

            assert_that(responded_coin_history['created_at'])\
                .is_equal_to(reformat_datetime(expected_coin_history.created_at))
            assert_that(responded_coin_history['updated_at'])\
                .is_equal_to(reformat_datetime(expected_coin_history.updated_at))

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
        response = self.client.post(f'/api/coin-histories/{expected_profile.id}/send-message/')

        # Then: 정상적으로 chat_link가 반환되고 user의 코인 개수가 비용만큼 줄어든다.
        created_coin_history = CoinHistory.objects.filter(user=user).last()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['chat_link']).is_equal_to(expected_profile.chat_link)
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
        response = self.client.post(f'/api/coin-histories/{expected_profile.id}/send-message/')

        # Then: 정상적으로 chat_link가 반환되고 user의 코인 개수는 줄어들지 않는다.
        created_coin_history = CoinHistory.objects.filter(user=user).last()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['chat_link']).is_equal_to(expected_profile.chat_link)
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
        response = self.client.post(f'/api/coin-histories/{expected_profile.id}/send-message/')

        # Then: 403 에러가 반환되고 user의 코인 개수는 줄어들지 않는다.
        created_coin_history = CoinHistory.objects.filter(user=user).last()

        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)
        assert_that(created_coin_history.rest_coin).is_equal_to(coin_history.rest_coin)
