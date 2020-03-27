from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker

from profiles.models import image_path


class SelfDateProfileImagePathTestCase(TestCase):
    def test_image_path(self):
        # Given: profile 하나가 주어진다.
        self_date_profile = baker.make('profiles.SelfDateProfile')
        file_name = 'image_name.png'

        # When: image_path method를 호출한다.
        path = image_path(self_date_profile, file_name)

        # Then: image가 저장될 경로가 반환된다.
        extension = file_name.split('.')[1]
        assert_that(path).is_equal_to(f'profiles/{self_date_profile.profile.user.email}/image.{extension}')
