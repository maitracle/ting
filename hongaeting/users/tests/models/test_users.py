from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker

from users.models import User


class UserTestCase(TestCase):

    def test_deactivate(self):
        # Given: user가 주어진다.
        user = baker.make('users.User',
                          email='origin_user_email@mail.com',
                          is_active=True)

        # When: user의 deactivate 함수를 실행한다.
        user.deactivate()

        # Then: user가 비활성화된다.
        deactivated_user = User.objects.get(id=user.id)
        assert_that(deactivated_user.is_active).is_false()

    def test_check_kakao_link(self):
        user = baker.make('users.User')

        user.check_kakao_link()

    # def test_check_kakao_link_return_true(self):
    #     # Given: 유효한 kakao talk open chat link를 가진 user가 주어진다.
    #     user = baker.make('users.User')
    #
    #     # When: check_kakao_link method를 실행한다.
    #     check_result = user.check_kakao_link()
    #
    #     # Then: True가 반환된다.
    #     assert_that(check_result).is_true()
    #
    # def test_check_kakao_link_return_false(self):
    #     # Given: 유효하지 않은 kakao talk open chat link를 가진 user가 주어진다.
    #     user = baker.make('users.User')
    #
    #     # When: check_kakao_link method를 실행한다.
    #     check_result = user.check_kakao_link()
    #
    #     # Then: True가 반환된다.
    #     assert_that(check_result).is_false()
