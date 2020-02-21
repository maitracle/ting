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
