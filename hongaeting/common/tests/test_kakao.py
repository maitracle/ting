from assertpy import assert_that
from django.test import TestCase

from common.KakaoClient import KakaoClient, KakaoClientWithTest


class KakaoTestCase(TestCase):
    def test_is_valid_kakao_link_should_return_true(self):
        # Given: valid한 kakao link가 주어진다.
        valid_link = KakaoClientWithTest.open_room_kakao_link

        # When: is_valid_kakao_link method를 호출한다.
        is_valid = KakaoClient.instance().is_valid_kakao_link(valid_link)

        # Then: true가 반환된다.
        assert_that(is_valid).is_true()

    def test_is_valid_kakao_link_should_return_false(self):
        # Given: invalid한 kakao link가 주어진다.
        invalid_link = KakaoClientWithTest.close_room_kakao_link

        # When: is_valid_kakao_link method를 호출한다.
        is_valid = KakaoClient.instance().is_valid_kakao_link(invalid_link)

        # Then: false가 반환된다.
        assert_that(is_valid).is_false()
