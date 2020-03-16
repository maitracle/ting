from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker

from profiles.models import profile_image_path


class ProfileImagePath(TestCase):
    def test_profile_image_path(self):
        # Given: profile 하나가 주어진다.
        profile = baker.make('profiles.Profile')
        file_name = 'image_name.png'

        # When: profile_image_path method를 호출한다.
        path = profile_image_path(profile, file_name)

        # Then: image가 저장될 경로가 반환된다.
        extension = file_name.split('.')[1]
        assert_that(path).is_equal_to(f'profiles/{profile.user.email}/image.{extension}')
