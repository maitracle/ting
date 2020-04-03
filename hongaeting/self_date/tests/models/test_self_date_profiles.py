from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker

from coins.models import CoinHistory
from common.constants import COST_COUNT


class SelfDateProfileTestCase(TestCase):
    def test_buy_right_for_target_self_date_profile(self):
        # Given: self_Date_profile, target_self_date_profile, rest_coin이 충분한 coin_history, right_type이 주어진다.
        self_date_profile = baker.make('self_date.SelfDateProfile')

        rest_coin = 30
        baker.make('coins.CoinHistory', rest_coin=rest_coin, profile=self_date_profile.profile)

        target_self_date_profile = baker.make('self_date.SelfDateProfile')

        right_type = CoinHistory.CHANGE_REASON.SELF_DATE_PROFILE_VIEW

        # When: self_date_profile의 buy_right_for_target_self_date_profile를 호출한다.
        self_date_profile_right = self_date_profile.buy_right_for_target_self_date_profile(target_self_date_profile,
                                                                                           right_type)

        # Then: 생성된 self_date_profile_right가 반환된다.
        assert_that(self_date_profile_right.buying_self_date_profile).is_equal_to(self_date_profile)
        assert_that(self_date_profile_right.target_self_date_profile).is_equal_to(target_self_date_profile)

        assert_that(self_date_profile_right.coin_history.profile).is_equal_to(self_date_profile.profile)
        assert_that(self_date_profile_right.coin_history.rest_coin).is_equal_to(rest_coin - COST_COUNT[right_type])
        assert_that(self_date_profile_right.coin_history.reason).is_equal_to(right_type)
        assert_that(self_date_profile_right.coin_history.message).is_equal_to(
            f'{target_self_date_profile.nickname}의 self date profile 조회')
