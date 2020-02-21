from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import Profile
from users.models import User


class UserViewSetTestCase(APITestCase):

    def test_should_create_profile_when_create_user(self):
        # Given: 만들어질 user에 관한 데이터가 주어진다.
        user_data = {
            "email": "testuser@test.com",
            "password": "password123",
            "nickname": "test",
            "gender": "MALE",
            "university": "HONGIK",
            "campus_location": "SEOUL",
            "university_email": "testuser@mail.hongik.ac.kr"
        }

        # When: user create api를 호출하여 회원가입을 한다.
        response = self.client.post('/api/users/', data=user_data)

        # Then: user와 profile이 만들어진다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        user = User.objects.get(email=user_data['email'])
        assert_that(user.email).is_equal_to(user_data['email'])
        assert_that(user.password).is_equal_to(user_data['password'])
        assert_that(user.university).is_equal_to(user_data['university'])
        assert_that(user.university_email).is_equal_to(user_data['university_email'])

        profile = Profile.objects.get(user=user.id)
        assert_that(profile.nickname).is_equal_to(user_data['nickname'])
        assert_that(profile.gender).is_equal_to(user_data['gender'])
        assert_that(profile.campus_location).is_equal_to(user_data['campus_location'])

    def test_should_not_create_when_profile_invalid(self):
        # Given: profile 관련 데이터가 invalid한 user 데이터가 주어진다.
        user_data = {
            "email": "testuser@test.com",
            "password": "password123",
            "nickname": "test",
            "gender": "",
            "university": "HONGIK",
            "campus_location": "SEOUL",
            "university_email": "testuser@mail.hongik.ac.kr"
        }

        # When: user create api를 호출하여 회원가입을 시도한다.
        response = self.client.post('/api/users/', data=user_data)

        # Then: user와 profile 둘 다 생성되지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=user_data['email'])
        assert_that(user).is_empty()
        profile = Profile.objects.filter(nickname=user_data['nickname'])
        assert_that(profile).is_empty()

    def test_should_not_create_when_user_invalid(self):
        # Given: user 관련 데이터가 invalid한 user 데이터가 주어진다.
        user_data = {
            "email": "testuser@test.com",
            "password": "",
            "nickname": "test",
            "gender": "MALE",
            "university": "HONGIK",
            "campus_location": "SEOUL",
            "university_email": "testuser@mail.hongik.ac.kr"
        }

        # When: user create api를 호출하여 회원가입을 시도한다.
        response = self.client.post('/api/users/', data=user_data)

        # Then: user와 profile 둘 다 생성되지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=user_data['email'])
        assert_that(user).is_empty()
        profile = Profile.objects.filter(nickname=user_data['nickname'])
        assert_that(profile).is_empty()

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
