from unittest.mock import patch

from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from common.utils import Email
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
            "scholarly_status": "ATTENDING",
            "university": "HONGIK",
            "campus_location": "SEOUL",
            "university_email": "testuser@mail.hongik.ac.kr"
        }
        user_code_length = 8

        # When: user create api를 호출하여 회원가입을 한다.
        response = self.client.post('/api/users/', data=user_data)

        # Then: user와 profile이 만들어진다.
        #       user의 user_code가 정상적으로 만들어진다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        user = User.objects.get(email=user_data['email'])
        assert_that(user.email).is_equal_to(user_data['email'])
        assert_that(user.password).is_equal_to(user_data['password'])
        assert_that(user.university).is_equal_to(user_data['university'])
        assert_that(user.university_email).is_equal_to(user_data['university_email'])
        assert_that(type(user.user_code)).is_equal_to(str)
        assert_that(user.user_code).is_length(user_code_length)

        profile = Profile.objects.get(user=user.id)
        assert_that(profile.nickname).is_equal_to(user_data['nickname'])
        assert_that(profile.gender).is_equal_to(user_data['gender'])
        assert_that(profile.scholarly_status).is_equal_to(user_data['scholarly_status'])
        assert_that(profile.campus_location).is_equal_to(user_data['campus_location'])

    def test_should_not_create_when_profile_invalid(self):
        # Given: profile 관련 데이터가 invalid한 user 데이터가 주어진다.
        user_data = {
            "email": "testuser@test.com",
            "password": "password123",
            "nickname": "test",
            "gender": "",
            "scholarly_status": "ATTENDING",
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
            "scholarly_status": "ATTENDING",
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
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/api/users/{user_id}/', data=changed_data)

        # Then: user data가 수정된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        user = User.objects.get(id=user_id)
        assert_that(user.email).is_equal_to(changed_data['email'])

    def test_should_fail_update_user(self):
        # Given: user 2개와 바꿀 user data가 주어진다
        original_email = 'origin_user_email@email.com'
        user = baker.make('users.User', email=original_email)
        user_id = user.id
        changed_data = {
            'email': 'changed_user_email@email.com'
        }

        another_user = baker.make('users.User')

        # When: 다른 유저의 user update api를 호출한다.
        self.client.force_authenticate(user=another_user)
        response = self.client.patch(f'/api/users/{user_id}/', data=changed_data)

        # Then: user data 수정을 실패한다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)

        user = User.objects.get(id=user_id)
        assert_that(user.email).is_equal_to(original_email)

    def test_should_delete_user(self):
        # Given: user가 주어진다
        user = baker.make('users.User', is_active=True)
        user_id = user.id

        # When: 주어진 user로 로그인 한 후, user delete api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/{user_id}/')

        # Then: user가 삭제된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_204_NO_CONTENT)
        assert_that(User.objects.get(id=user_id).is_active).is_false()

    def test_should_fail_delete_user(self):
        # Given: user가 주어진다
        user = baker.make('users.User', is_active=True)
        another_user = baker.make('users.User')
        user_id = user.id

        # When: 주어진 user로 로그인 한 후, user delete api를 호출한다.
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(f'/api/users/{user_id}/')

        # Then: user삭제를 실패한다.
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)
        assert_that(User.objects.get(id=user_id).is_active).is_true()

    @patch.object(Email, 'send_email')
    def test_should_check_university(self, send_email):
        # Given: user와 등록할 user의 학교 이메일이 주어진다.
        user = baker.make('users.User')
        user_id = user.id
        data = {
            "university_email": "test@test.com"
        }

        # When: 주어진 user로 로그인 한 후, 학교 이메일 정보로 check-univ api를 호출한다.
        self.client.force_authenticate(user=user)
        response = self.client.patch(f'/api/users/{user_id}/check-univ/', data)

        # Then: user의 학교 이메일이 update되고 학교 이메일로 메일이 전송된다.
        user = User.objects.get(university_email=data['university_email'])
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(user.university_email).is_equal_to(data['university_email'])
        send_email.assert_called_once()

    @patch.object(Email, 'send_email')
    def test_should_fail_check_university(self, send_email):
        # Given: user와 등록할 user의 학교 이메일이 주어진다.
        user = baker.make('users.User')
        another_user = baker.make('users.User')
        data = {
            "university_email": "test@test.com"
        }

        # When: 주어진 user로 로그인 한 후, 학교 이메일 정보로 check-univ api를 호출한다.
        self.client.force_authenticate(user=another_user)
        response = self.client.patch(f'/api/users/{user.id}/check-univ/', data)

        # Then: user의 학교 이메일이 update되고 학교 이메일로 메일이 전송된다.
        user = User.objects.get(id=user.id)
        send_email.assert_not_called()
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)
        assert_that(user.university_email).is_equal_to(user.university_email)
