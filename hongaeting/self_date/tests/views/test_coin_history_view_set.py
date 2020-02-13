from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from self_date.models import CoinHistory


class CoinHistoryTestCase(APITestCase):
    def test_should_get_list(self):
        # Given: user 1명이 생성되고 그 유저의 coin-history가 생성된다.
        user = baker.make('users.User')
        coin_history_quantity = 3
        baker.make('self_date.CoinHistory', user=user, _quantity=coin_history_quantity)

        # When: user가 coin_history_list api 호출
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/coin-histories/')

        # Then: response값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(coin_history_quantity)
        for i in range(coin_history_quantity):
            assert_that(response.data[i]['user']).is_equal_to(user.id)


    def test_should_consume(self):
        # Given: user 1명과 그의 Signup coin_history가 생성된다.
        user = baker.make('users.User')
        user_rest_coin = 2
        baker.make('self_date.CoinHistory', user=user, reason=CoinHistory.CHANGE_REASON.SIGNUP,
                   rest_coin=user_rest_coin)

        # When: user가 consume api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/coin-histories/consume/')

        # Then: response값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.data['rest_coin']).is_equal_to(user_rest_coin - 1)
        assert_that(CoinHistory.objects.last().rest_coin).is_equal_to(user_rest_coin - 1)

    def test_should_refund_coin_history(self):
        # Given: user 1명과 그의 Signup coin_history가 생성된다.
        user = baker.make('users.User')
        user_rest_coin = 2
        baker.make('self_date.CoinHistory', user=user, reason=CoinHistory.CHANGE_REASON.SIGNUP,
                   rest_coin=user_rest_coin)

        # When: user가 refund api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/coin-histories/refund/')

        # Then: response값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.data['rest_coin']).is_equal_to(user_rest_coin + 1)
        assert_that(CoinHistory.objects.last().rest_coin).is_equal_to(user_rest_coin + 1)
