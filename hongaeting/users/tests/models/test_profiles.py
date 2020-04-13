import datetime

from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker


class ProfileTestCase(TestCase):
    def test_age_property(self):
        # Given: profile이 주어진다.
        year_delta = 20
        profile = baker.make('users.Profile',
                             born_year=datetime.datetime.now().year - year_delta)

        # When: user의 deactivate 함수를 실행한다.
        returned_age = profile.age

        # Then: user가 비활성화된다.
        assert_that(returned_age).is_equal_to(year_delta + 1)
