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

    def test_set_user_code_method(self):
        # Given: usercode가 없는 user가 1개 생성된다.
        user = baker.make('users.User', user_code='')
        user_code_length = 8

        # When: set_user_code 메소드를 실행한다.
        user.set_user_code()

        # Then: user에게 user_code가 생성된다.
        assert_that(type(user.user_code)).is_equal_to(str)
        assert_that(user.user_code).is_length(user_code_length)
