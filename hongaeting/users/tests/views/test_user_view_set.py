from assertpy import assert_that
from model_bakery import baker
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
        response = self.client.post('/api/users/users/', data=user_data)

        # Then: 요청한 data로 user가 만들어진다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        user = User.objects.get(username=user_data['username'])
        assert_that(user.username).is_equal_to(user_data['username'])
        assert_that(user.password).is_equal_to(user_data['password'])
        assert_that(user.email).is_equal_to(user_data['email'])

    def test_should_update_user(self):
        # Given: user와 바꿀 user data가 주어진다
        user = baker.make('users.User',
                          username='origin_user_name')

        user_id = user.id

        changed_data = {
            'username': 'changed_user_name'
        }

        # When: user update api를 호출한다.
        response = self.client.patch(f'/api/users/users/{user_id}/', data=changed_data)

        # Then: user data가 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        user = User.objects.get(id=user_id)
        assert_that(user.username).is_equal_to(changed_data['username'])


    def test_should_delete_user(self):
        # Given: user가 주어진다
        user = baker.make('users.User')
        user_id = user.id

        # When: 주어진 user로 로그인 한 후, user delete api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/users/{user_id}/')

        # Then: user가 삭제된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_204_NO_CONTENT)
