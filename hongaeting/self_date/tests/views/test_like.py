from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from self_date.models import SelfDateProfile
from self_date.models import SelfDateLike


class LikeTestCase(APITestCase):
    def test_should_get_like_list(self):
        # Given: self_date_profile을 가진 user 1명, liked_self_date_profile 3개, self_date_like 3개가 주어진다.
        self_date_profile = baker.make('self_date.SelfDateProfile')
        liked_self_date_profile_quantity = 3
        liked_self_date_profile_list = baker.make('self_date.SelfDateProfile',
                                                  _quantity=liked_self_date_profile_quantity)
        self_date_like_list = [
            baker.make('self_date.SelfDateLike',
                       self_date_profile=self_date_profile, liked_self_date_profile=liked_self_date_profile)
            for liked_self_date_profile in liked_self_date_profile_list
        ]

        # When: sef_date_like_list api를 호출한다
        self.client.force_authenticate(user=self_date_profile.profile.user)
        response = self.client.get('/api/likes/')

        # Then: response값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(liked_self_date_profile_quantity)
        for response_item, expected_item in zip(response.data, self_date_like_list):
            assert_that(response_item['self_date_profile']).is_equal_to(self_date_profile.id)
            assert_that(response_item['liked_self_date_profile']).is_equal_to(expected_item.liked_self_date_profile.id)

    def test_should_get_liked_list(self):
        # Given: liked_self_date_profile을 가진 user 1명과 self_date_profile 3개 self_date_like 3개가 주어진다.
        liked_self_date_profile = baker.make('self_date.SelfDateProfile')
        self_date_profile_quantity = 3
        self_date_profile_list = baker.make('self_date.SelfDateProfile', _quantity=self_date_profile_quantity)
        like_list = [
            baker.make('self_date.SelfDateLike', self_date_profile=self_date_profile,
                       liked_self_date_profile=liked_self_date_profile)
            for self_date_profile in self_date_profile_list
        ]

        # When: liked_self_date_profile을 가진 user가 self_date_like_list api를 호출한다
        self.client.force_authenticate(user=liked_self_date_profile.profile.user)
        response = self.client.get('/api/likes/liked/')

        # Then: response값이 정상적으로 온다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data).is_length(self_date_profile_quantity)

        for response_item, expected_item in zip(response.data, like_list):
            assert_that(response_item['liked_self_date_profile']).is_equal_to(expected_item.liked_self_date_profile.id)
            assert_that(response_item['self_date_profile']).is_equal_to(expected_item.self_date_profile.id)

    def test_should_create_like(self):
        # Given : self_date_profile을 가진 user 1명과 좋아요할 프로필이 주어진다.
        self_date_profile = baker.make('self_date.SelfDateProfile')
        liked_self_date_profile = baker.make('self_date.SelfDateProfile')
        like_data = {
            'self_date_profile': self_date_profile.id,
            'liked_self_date_profile': liked_self_date_profile.id,
        }

        # When: user가 like_create api를 호출한다.
        self.client.force_authenticate(user=self_date_profile.profile.user)
        response = self.client.post('/api/likes/', data=like_data)

        # Then: like 모델이 정상적으로 생성된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)
        assert_that(response.data['self_date_profile']).is_equal_to(self_date_profile.id)
        assert_that(response.data['liked_self_date_profile']).is_equal_to(liked_self_date_profile.id)

    def test_should_destroy(self):
        # Given: self_date_profile을 가진 user 1명과 like가 하나 주어진다.
        self_date_profile = baker.make('self_date.SelfDateProfile')
        like = baker.make('self_date.SelfDateLike', self_date_profile=self_date_profile)
        like_id = like.id

        # When: user가 destroy api를 호출한다.
        self.client.force_authenticate(user=self_date_profile.profile.user)
        response = self.client.delete(f'/api/likes/{like_id}/')

        # Then: like 모델이 삭제된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_204_NO_CONTENT)
        assert_that(SelfDateLike.objects.filter(id=like_id)).is_empty()

