from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker

from common.Kakao import KakaoWithTest
from common.constants import COST_COUNT, COIN_CHANGE_REASON


class SelfDateProfileTestCase(TestCase):
    def test_buy_right_for_target_self_date_profile(self):
        # Given: self_Date_profile, target_self_date_profile, rest_coin이 충분한 coin_history, right_type이 주어진다.
        self_date_profile = baker.make('self_date.SelfDateProfile')

        rest_coin = 30
        baker.make('coins.CoinHistory', rest_coin=rest_coin, profile=self_date_profile.profile)

        target_self_date_profile = baker.make('self_date.SelfDateProfile')

        right_type = COIN_CHANGE_REASON.SELF_DATE_PROFILE_VIEW

        # When: self_date_profile의 buy_right_for_target_self_date_profile를 호출한다.
        self_date_profile_right = self_date_profile.buy_right_for_target_self_date_profile(target_self_date_profile,
                                                                                           right_type)

        # Then: 생성된 self_date_profile_right가 반환된다.
        assert_that(self_date_profile_right.buying_self_date_profile).is_equal_to(self_date_profile)
        assert_that(self_date_profile_right.target_self_date_profile).is_equal_to(target_self_date_profile)
        assert_that(self_date_profile_right.right_type).is_equal_to(right_type)

        assert_that(self_date_profile_right.coin_history.profile).is_equal_to(self_date_profile.profile)
        assert_that(self_date_profile_right.coin_history.rest_coin).is_equal_to(rest_coin - COST_COUNT[right_type])
        assert_that(self_date_profile_right.coin_history.reason).is_equal_to(right_type)
        assert_that(self_date_profile_right.coin_history.message).is_equal_to(
            f'{target_self_date_profile.nickname}의 self date profile 조회')

    def test_is_valid_chat_link_should_be_true(self):
        # Given: valid한 kakao link를 가진 self_date_profile이 주어진다.
        valid_kakao_link = KakaoWithTest.valid_kakao_link
        self_date_profile = baker.make('self_date.SelfDateProfile', chat_link=valid_kakao_link)

        # When: is_valid_chat_link property를 확인한다.
        is_valid = self_date_profile.is_valid_chat_link

        # Then: true가 반환된다.
        assert_that(is_valid).is_true()

    def test_is_valid_chat_link_should_be_false(self):
        # Given: invalid한 kakao link를 가진 self_date_profile이 주어진다.
        valid_kakao_link = KakaoWithTest.invalid_kakao_link
        self_date_profile = baker.make('self_date.SelfDateProfile', chat_link=valid_kakao_link)

        # When: is_valid_chat_link property를 확인한다.
        is_valid = self_date_profile.is_valid_chat_link

        # Then: false가 반환된다.
        assert_that(is_valid).is_false()
