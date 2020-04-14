import datetime

from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker

from common.constants import REWORD_COUNT, COIN_CHANGE_REASON


class ProfileTestCase(TestCase):
    def test_age_property(self):
        # Given: profile이 주어진다.
        year_delta = 20
        profile = baker.make('users.Profile',
                             born_year=datetime.datetime.now().year - year_delta)

        # When: profile의 age property를 확인한다.
        returned_age = profile.age

        # Then: 나이 property가 반환된다.
        assert_that(returned_age).is_equal_to(year_delta + 1)

    def test_get_rest_coin_when_coin_history_exists(self):
        # Given: coin_history가 있는 profile가 주어진다.
        profile = baker.make('users.Profile')

        expected_rest_coin = 10
        baker.make('coins.CoinHistory', rest_coin=expected_rest_coin, profile=profile)

        # When: profile의 get_test_coin method를 실행한다.
        rest_coin = profile.get_rest_coin()

        # Then: 현재 남은 코인 개수가 반환된다.
        assert_that(rest_coin).is_equal_to(expected_rest_coin)

    def test_get_rest_coin_when_coin_history_empty(self):
        # Given: coin_history가 없는 profile가 주어진다.
        profile = baker.make('users.Profile')

        # When: profile의 get_test_coin method를 실행한다.
        rest_coin = profile.get_rest_coin()

        # Then: 현재 남은 코인 개수가 반환된다.
        assert_that(rest_coin).is_equal_to(0)

    def test_earn_coin(self):
        # Given: coin_history가 있는 profile가 주어진다.
        #        생성할 coin history에 대한 정보가 주어진다.
        profile = baker.make('users.Profile')

        rest_coin = 10
        baker.make('coins.CoinHistory', rest_coin=rest_coin, profile=profile)

        expected_coin_history_data = {
            'earn_coin_count': REWORD_COUNT['CONFIRM_USER'],
            'reason': COIN_CHANGE_REASON.CONFIRM_USER,
            'message': '학교 인증 완료 보상',
        }

        # When: profile의 get_coin method를 실행한다.
        created_coin_history = profile.earn_coin(expected_coin_history_data['earn_coin_count'],
                                                 expected_coin_history_data['reason'],
                                                 expected_coin_history_data['message'])

        # Then: coin_history가 생성된다.
        assert_that(created_coin_history.profile).is_equal_to(profile)
        assert_that(created_coin_history.rest_coin).is_equal_to(
            rest_coin + expected_coin_history_data['earn_coin_count'])
        assert_that(created_coin_history.reason).is_equal_to(expected_coin_history_data['reason'])
        assert_that(created_coin_history.message).is_equal_to(expected_coin_history_data['message'])

    def test_earn_coin_when_coin_history_is_none(self):
        # Given: coin_history가 없는 profile가 주어진다.
        #        생성할 coin history에 대한 정보가 주어진다.
        profile = baker.make('users.Profile')

        expected_coin_history_data = {
            'earn_coin_count': REWORD_COUNT['CONFIRM_USER'],
            'reason': COIN_CHANGE_REASON.CONFIRM_USER,
            'message': '학교 인증 완료 보상',
        }

        # When: profile의 get_coin method를 실행한다.
        created_coin_history = profile.earn_coin(expected_coin_history_data['earn_coin_count'],
                                                 expected_coin_history_data['reason'],
                                                 expected_coin_history_data['message'])

        # Then: coin_history가 생성된다.
        assert_that(created_coin_history.profile).is_equal_to(profile)
        assert_that(created_coin_history.rest_coin).is_equal_to(expected_coin_history_data['earn_coin_count'])
        assert_that(created_coin_history.reason).is_equal_to(expected_coin_history_data['reason'])
        assert_that(created_coin_history.message).is_equal_to(expected_coin_history_data['message'])
