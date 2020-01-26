from assertpy import assert_that
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserViewSetTestCase(APITestCase):

    def test_should_create_user(self):
        # Given: user data가 주어진다.
        user_data = {
            'username': 'test_username',
            'password': 'test_password',
            'email': 'test_email@email.com',
        }

        # When: user create api를 호출한다.
        response = self.client.post('/api/users/', data=user_data)

        # Then: 요청한 data로 user가 만들어진다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        user = User.objects.get(username=user_data['username'])
        assert_that(user.username).is_equal_to(user_data['username'])
        assert_that(user.password).is_equal_to(user_data['password'])
        assert_that(user.email).is_equal_to(user_data['email'])
