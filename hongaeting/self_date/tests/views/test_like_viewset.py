from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from self_date.models import Like


class LikeTestCase(APITestCase):

    def test_create_like(self):
        # Given: user가 2명 주어진다.
        user = baker.make('users.User')
        liked_user = baker.make('users.User')

        # When: user1 이 like-create api 를 호출한다.

        # Then : user1-user2의 like가 존재하는지 확인한다. 없으면 요청한 data로 like가 만들어진다.

    def test_delete_like(self):
        # Given : user가 2명 주어진다.
        user = baker.make('users.User')
        liked_user = baker.make('users.User')

        # When: user1 이 기존에 좋아요를 했던 user2를
        # like-delete api 를 호출한다.

        # Then : user1의 like가 삭제된다.

    def test_should_get_like_list(self):
        # Given: user가 2명과 like 1개가 주어진다.
        user = baker.make('users.User')
        liked_user_quantity = 3
        liked_user_list = baker.make('users.User', _quantity=liked_user_quantity)
        like_list = [
            baker.make('self_date.Like', user=user, liked_user=liked_user) for liked_user in liked_user_list
        ]

        # When: user가 like_list api를 호출한다
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/likes/')

        # Then: response값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(liked_user_quantity)
        for response_item, expected_item in zip(response.data, like_list):
            assert_that(response_item['user']).is_equal_to(user.id)
            assert_that(response_item['liked_user']).is_equal_to(expected_item.liked_user.id)

    def test_should_get_liked_list(self):
        # Given : user가 2명과 like 1개가 주어진다.
        liked_user = baker.make('users.User')
        user_quantity = 3
        user_list = baker.make('users.User', _quantity=user_quantity)
        like_list = [
            baker.make('self_date.Like', user=user, liked_user=liked_user) for user in user_list
        ]

        # When: user가 like_list api를 호출한다
        self.client.force_authenticate(user=liked_user)
        response = self.client.get('/api/likes/liked/')

        # Then: response값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(user_quantity)

        for response_item, expected_item in zip(response.data, like_list):
            assert_that(response_item['user']).is_equal_to(expected_item.user.id)
            assert_that(response_item['liked_user']).is_equal_to(expected_item.liked_user.id)

    def test_should_create_like(self):
        # Given : user가 2명 주어진다.
        user = baker.make('users.User', _quantity=2)
        like_data = {
            "user" : user[0].id,
            "liked_user" : user[1].id,
        }

        # When: user가 like_create api를 호출한다.
        self.client.force_authenticate(user=user[0])
        response = self.client.post('/api/likes/create-like/', data=like_data)

        # Then: like 모델이 정상적으로 생성
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.data["user"]).is_equal_to(user[0].id)
        assert_that(response.data["liked_user"]).is_equal_to(user[1].id)

    def test_should_destroy_test(self):
        # Given: like 모델이 하나 주어진다.
        user = baker.make('users.User')
        like = baker.make('self_date.Like')
        like_id = like.id

        # When: user가 destroy api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/likes/{like_id}/')

        # Then: like 모델이 삭제된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_204_NO_CONTENT)
        assert_that(Like.objects.filter(id=like_id)).is_empty()