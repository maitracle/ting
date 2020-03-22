from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker

from users.models import student_id_card_image_path


class StudentIdCardImagePath(TestCase):
    def test_student_id_card_image_path(self):
        # Given: profile 하나가 주어진다.
        user = baker.make('users.User')
        file_name = 'image_name.png'

        # When: profile_image_path method를 호출한다.
        path = student_id_card_image_path(user, file_name)

        # Then: image가 저장될 경로가 반환된다.
        extension = file_name.split('.')[1]
        assert_that(path).is_equal_to(f'id_cards/{user.email}/image.{extension}')
