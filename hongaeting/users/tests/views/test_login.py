from assertpy import assert_that
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class JwtTestCase(APITestCase):

    def test_should_get_jwt_token(self):
        # Given: user가 주어진다.
        username = 'test_username'
        password = 'test_password'
        User.objects.create_user(username=username, password=password)

        # When: jwt token을 요청한다.
        payload = {
            'username': username,
            'password': password,
        }
        response = self.client.post('/api/tokens/', data=payload)

        # Then: access token, refresh token이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that('refresh' in response.data).is_true()
        assert_that('access' in response.data).is_true()

    def test_should_refresh_jwt_token(self):
        # Given: user와 user의 refresh token이 주어진다.
        username = 'test_username'
        password = 'test_password'
        user = User.objects.create_user(username=username, password=password)

        refresh_token = str(RefreshToken.for_user(user))

        # When: token refresh api를 요청한다.
        payload = {
            'refresh': refresh_token,
        }
        response = self.client.post('/api/tokens/refresh/', data=payload)

        # Then: access token이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that('access' in response.data).is_true()
