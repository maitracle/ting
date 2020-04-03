from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.utils import reformat_datetime


class CoinHistoryTestCase(APITestCase):
    def test_should_get_list(self):
        # Given: profile과 coin-history가 주어진다.
        profile = baker.make('users.Profile')
        coin_history_quantity = 3
        expected_coin_histories = baker.make('coins.CoinHistory', profile=profile, _quantity=coin_history_quantity)

        # When: user가 coin_history_list api 호출
        self.client.force_authenticate(user=profile.user)
        response = self.client.get('/api/coin-histories/')

        # Then: status_code 200이 반환된다.
        #       coin history list가 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(coin_history_quantity)

        for responded_coin_history, expected_coin_history in zip(response.data, reversed(expected_coin_histories)):
            assert_that(responded_coin_history['profile']).is_equal_to(profile.id)
            assert_that(responded_coin_history['rest_coin']).is_equal_to(expected_coin_history.rest_coin)
            assert_that(responded_coin_history['reason']).is_equal_to(expected_coin_history.reason)
            assert_that(responded_coin_history['message']).is_equal_to(expected_coin_history.message)

            assert_that(responded_coin_history['created_at']) \
                .is_equal_to(reformat_datetime(expected_coin_history.created_at))
            assert_that(responded_coin_history['updated_at']) \
                .is_equal_to(reformat_datetime(expected_coin_history.updated_at))
