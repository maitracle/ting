from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserViewSetTestCase(APITestCase):

    def test_should_create_user(self):
        # Given: user data가 주어진다.
        user_data = {
            'email': 'test_email@email.com',
            'password': 'test_password',
        }

        # When: user create api를 호출한다.
        response = self.client.post('/api/users/', data=user_data)

        # Then: 요청한 data로 user가 만들어진다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        user = User.objects.get(email=user_data['email'])
        assert_that(user.email).is_equal_to(user_data['email'])
        assert_that(user.password).is_equal_to(user_data['password'])

    def test_should_update_user(self):
        # Given: user와 바꿀 user data가 주어진다
        user = baker.make('users.User',
                          email='origin_user_email@email.com')

        user_id = user.id

        changed_data = {
            'email': 'changed_user_email@email.com'
        }

        # When: user update api를 호출한다.
        response = self.client.patch(f'/api/users/{user_id}/', data=changed_data)

        # Then: user data가 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        user = User.objects.get(id=user_id)
        assert_that(user.email).is_equal_to(changed_data['email'])

    def test_should_delete_user(self):
        # Given: user가 주어진다
        user = baker.make('users.User')
        user_id = user.id

        # When: 주어진 user로 로그인 한 후, user delete api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/{user_id}/')

        # Then: user가 삭제된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_204_NO_CONTENT)
