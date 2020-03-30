from assertpy import assert_that
from django.core.exceptions import ValidationError
from django.test import TestCase
from model_bakery import baker

from common.constants import UNIVERSITY_CHOICES
from users.models import Profile


class UserTestCase(TestCase):
    def test_clean_method(self):
        # given: 소속 대학과 캠퍼스 위치가 부합하지 않은 Profile이 생성된다.
        profile = baker.make(
            'users.Profile',
            university=UNIVERSITY_CHOICES.HONGIK,
            campus_location=Profile.CAMPUS_LOCATION_CHOICES.INTERNATIONAL
        )

        # when: Profile.clean() 메소드를 실행한다.
        try:
            profile.clean()

        # then: ValidationError가 잡힌다.
        except Exception as err:
            assert_that(type(err)).is_equal_to(ValidationError)
            assert_that(err.message).is_equal_to('Not Valid Campus')
