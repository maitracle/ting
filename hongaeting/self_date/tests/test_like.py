from assertpy import assert_that
from django.test import TestCase
from model_bakery import baker

from self_date.models import Like
from users.models import User

class LikeTestCase(TestCase):

    def test_create_like(self):
        # Given: user가 2명 주어진다.
        user = baker.make('users.User')
        liked_user=baker.make('users.User')

        # When: user1 이 like-create api 를 호출한다.

        # Then : user1-user2의 like가 존재하는지 확인한다. 없으면 요청한 data로 like가 만들어진다.


    def test_delete_like(self):
        #Given : user가 2명 주어진다.
        user = baker.make('users.User')
        liked_user = baker.make('users.User')

        # When: user1 이 기존에 좋아요를 했던 user2를
        # like-delete api 를 호출한다.


        # Then : user1의 like가 삭제된다.