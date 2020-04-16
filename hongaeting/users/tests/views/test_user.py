import json
import os
from unittest.mock import patch

from PIL import Image
from assertpy import assert_that
from django.conf import settings
from django.contrib.auth.hashers import make_password
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from coins.models import CoinHistory
from common.constants import REWORD_COUNT, COIN_CHANGE_REASON
from common.decorator import delete_media_root
from common.utils import Email, reformat_datetime
from users.models import User


class UserViewSetTestCase(APITestCase):

    def test_create_user(self):
        # Given: 만들어질 user에 관한 데이터가 주어진다.
        user_data = {
            'email': 'testuser@test.com',
            'password': 'password123',
        }
        user_code_length = 8

        # When: user create api를 호출하여 회원가입을 한다.
        response = self.client.post('/api/users/', data=json.dumps(user_data), content_type='application/json')

        # Then: 만들어진 User가 반환된다.
        #       access token, refresh token이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_201_CREATED)

        assert_that('access' in response.data).is_true()
        assert_that('refresh' in response.data).is_true()

        user = User.objects.get(email=user_data['email'])

        assert_that(response.data['user']['id']).is_equal_to(user.id)
        assert_that(response.data['user']['email']).is_equal_to(user_data['email'])
        hashed_password_prefix = 'pbkdf2_sha256$150000$'
        assert_that(response.data['user']['password'].startswith(hashed_password_prefix)).is_true()
        assert_that(response.data['user']['is_confirmed_student']).is_false()
        assert_that(user.user_code).is_length(user_code_length)

    def test_should_not_create(self):
        # Given: 비밀번호가 invalid한 user 데이터가 주어진다.
        user_data = {
            'email': 'testuser@test.com',
            'password': '',
        }

        # When: user create api를 호출하여 회원가입을 시도한다.
        response = self.client.post('/api/users/', data=user_data)

        # Then: user와 profile 둘 다 생성되지 않는다.
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=user_data['email'])
        assert_that(user).is_empty()

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

    @delete_media_root
    def test_should_update_student_id_card_image_field(self):
        # Given: user와 수정할 image file이 주어진다.
        user = baker.make('users.User',
                          email='origin_user_email@email.com')
        user_id = user.id

        try:
            image = Image.new('RGB', (100, 100))
            image.save('tmp_image.jpg')
            tmp_file = open('tmp_image.jpg', 'rb')
            update_data = {
                'student_id_card_image': tmp_file
            }

            # When: user update api를 호출한다.
            self.client.force_authenticate(user=user)
            response = self.client.patch(f'/api/users/{user_id}/', data=update_data)

            # Then: user의 student_id_card_image가 반환된다.
            assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

            email_name, email_domain = user.email.split('@')
            expected_image_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/' \
                                 f'{settings.MEDIA_ROOT}/id_cards/{email_name}%40{email_domain}/image.jpg'
            assert_that(response.data['student_id_card_image']).is_equal_to(expected_image_url)

        finally:
            # 임시로 만든 이미지 파일을 삭제한다.
            tmp_file.close()
            if os.path.exists('tmp_image.jpg'):
                os.remove('tmp_image.jpg')

    def test_should_fail_update_user_for_another_user(self):
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

    def test_should_get_my_user_profile_coin_history(self):
        # Given: user와 profile, coin_history가 주어진다.
        expected_user = baker.make('users.User')
        expected_profile = baker.make('users.Profile', user=expected_user)
        coin_history_quantity = 5
        expected_coin_history_list = baker.make('coins.CoinHistory', profile=expected_profile,
                                                _quantity=coin_history_quantity)

        # When: user가 my profile api를 호출한다.
        self.client.force_authenticate(user=expected_user)
        response = self.client.get(f'/api/users/my/')

        # Then: 자신의 user, profile, coin_history가 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        self._assert_user(response.data['user'], expected_user)
        self._assert_profile(response.data['profile'], expected_profile)

        assert_that(response.data['coin_history']).is_length(coin_history_quantity)
        for response_coin_history, expected_coin_history in \
                zip(response.data['coin_history'], reversed(expected_coin_history_list)):
            self._assert_coin_history(response_coin_history, expected_coin_history)

    def test_should_get_my_user_without_profile(self):
        # Given: user와 profile, coin_history가 주어진다.
        expected_user = baker.make('users.User')

        # When: user가 my profile api를 호출한다.
        self.client.force_authenticate(user=expected_user)
        response = self.client.get(f'/api/users/my/')

        # Then: 자신의 user, profile, coin_history가 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        self._assert_user(response.data['user'], expected_user)
        assert_that(response.data['profile']).is_none()
        assert_that(response.data['coin_history']).is_equal_to([])

    @patch.object(Email, 'send_email')
    def test_should_check_university(self, send_email):
        # Given: user와 등록할 user의 학교 이메일이 주어진다.
        user = baker.make('users.User')
        baker.make('users.Profile', user=user)
        user_id = user.id
        data = {
            'university_email': 'test@test.com'
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
            'university_email': 'test@test.com'
        }

        # When: 주어진 user로 로그인 한 후, 학교 이메일 정보로 check-univ api를 호출한다.
        self.client.force_authenticate(user=another_user)
        response = self.client.patch(f'/api/users/{user.id}/check-univ/', data)

        # Then: user의 학교 이메일이 update되고 학교 이메일로 메일이 전송된다.
        user = User.objects.get(id=user.id)
        send_email.assert_not_called()
        assert_that(response.status_code).is_equal_to(status.HTTP_403_FORBIDDEN)
        assert_that(user.university_email).is_equal_to(user.university_email)

    def test_confirm_user(self):
        # Given: user, profile과 user의 user_code가 제공된다.
        user_code = 'abcdefgh'
        user = baker.make('users.user', user_code=user_code)
        profile = baker.make('users.Profile', user=user)
        assert_that(user.is_confirmed_student).is_false()
        data = {
            'user_code': user_code,
        }

        origin_coin_history_count = profile.get_rest_coin()

        # When: confirm-user api를 호출한다.
        response = self.client.post('/api/users/confirm-user/', data=data)

        # Then: status code 200이 반환된다.
        #       user의 is_confirmed field가 True로 수정된다.
        #       confirm user coin_history가 생성된다.
        user = User.objects.get(user_code=user_code)
        assert_that(user.is_confirmed_student).is_true()
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        coin_history = user.profile.coin_histories.last()
        assert_that(coin_history.rest_coin).is_equal_to(origin_coin_history_count + REWORD_COUNT['CONFIRM_USER'])
        assert_that(coin_history.reason).is_equal_to(COIN_CHANGE_REASON.CONFIRM_USER)
        assert_that(coin_history.message).is_equal_to('학생 인증으로 인한 coin 지급')

    def test_should_not_confirm_user(self):
        # Given: user, profile 1개와 존재하지 않는 user_code가 하나 주어진다.
        not_exist_user_code = 'abcdefgh'
        user = baker.make('users.user', user_code='testtest')
        baker.make('users.Profile', user=user)
        data = {
            'user_code': not_exist_user_code,
        }

        origin_coin_history_ids = CoinHistory.objects.all().values_list('pk', flat=True)

        # When: confirm-user api를 호출한다.
        response = self.client.post('/api/users/confirm-user/', data=data)

        # Then: 찾고자 하는 user가 없다는 오류가 발생하고, 기존 유저는 인증되지 않는다.
        #       coin_history가 새로 생성되지 않는다.
        user = User.objects.get(user_code='testtest')
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)
        assert_that(user.is_confirmed_student).is_false()

        assert_that(CoinHistory.objects.all().exclude(id__in=origin_coin_history_ids).exists()).is_false()

    def test_confirm_user_without_profile(self):
        # Given: user와 user의 user_code가 제공된다.
        user_code = 'abcdefgh'
        user = baker.make('users.user', user_code=user_code)
        assert_that(user.is_confirmed_student).is_false()
        data = {
            'user_code': user_code,
        }

        origin_coin_history_ids = CoinHistory.objects.all().values_list('pk', flat=True)

        # When: confirm-user api를 호출한다.
        response = self.client.post('/api/users/confirm-user/', data=data)

        # Then: user의 is_confirmed field가 True로 바뀐 후 정상적으로 응답이 도달한다.
        #       coin_history가 새로 생성되지 않는다.
        user = User.objects.get(user_code=user_code)
        assert_that(user.is_confirmed_student).is_true()
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

        assert_that(CoinHistory.objects.all().exclude(id__in=origin_coin_history_ids).exists()).is_false()

    def test_should_get_jwt_token_user_profile_and_coin_history(self):
        # Given: user, profile, coin_history, 올바른 email, password가 주어진다.
        password_string = 'password'
        user = baker.make('users.User', password=make_password(password_string), is_active=True)
        profile = baker.make('users.Profile', user=user)

        coin_history_quantity = 5
        coin_history_list = baker.make('coins.CoinHistory', profile=profile, _quantity=coin_history_quantity)

        # When: login api를 호출한다.
        payload = {
            'email': user.email,
            'password': password_string,
        }
        response = self.client.post('/api/users/tokens/', data=payload)

        # Then: access token, refresh token, user, profile, coin_history가 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that('access' in response.data).is_true()
        assert_that('refresh' in response.data).is_true()

        self._assert_user(response.data['user'], user)
        self._assert_profile(response.data['profile'], profile)

        assert_that(response.data['coin_history']).is_length(coin_history_quantity)
        for response_coin_history, expected_coin_history in \
                zip(response.data['coin_history'], reversed(coin_history_list)):
            self._assert_coin_history(response_coin_history, expected_coin_history)

    def test_should_get_jwt_token_and_user_without_profile(self):
        # Given: user, 올바른 email, password가 주어진다.
        password_string = 'password'
        user = baker.make('users.User', password=make_password(password_string), is_active=True)

        # When: login api를 호출한다.
        payload = {
            'email': user.email,
            'password': password_string,
        }
        response = self.client.post('/api/users/tokens/', data=payload)

        # Then: access token, refresh token, user가 반환된다.
        #       profile, coin_history는 None이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that('access' in response.data).is_true()
        assert_that('refresh' in response.data).is_true()

        self._assert_user(response.data['user'], user)
        assert_that(response.data['profile']).is_none()
        assert_that(response.data['coin_history']).is_equal_to([])

    @staticmethod
    def _assert_user(responsed_user, expected_user):
        assert_that(responsed_user['id']).is_equal_to(expected_user.id)
        assert_that(responsed_user['email']).is_equal_to(expected_user.email)

        assert_that(responsed_user['user_code']).is_equal_to(expected_user.user_code)
        assert_that(responsed_user['is_confirmed_student']).is_equal_to(expected_user.is_confirmed_student)

    @staticmethod
    def _assert_profile(responsed_profile, expected_profile):
        assert_that(responsed_profile['id']).is_equal_to(expected_profile.id)
        assert_that(responsed_profile['user']).is_equal_to(expected_profile.user.id)
        assert_that(responsed_profile['gender']).is_equal_to(expected_profile.gender)
        assert_that(responsed_profile['age']).is_equal_to(expected_profile.age)
        assert_that(responsed_profile['university']).is_equal_to(expected_profile.university)
        assert_that(responsed_profile['campus_location']).is_equal_to(expected_profile.campus_location)
        assert_that(responsed_profile['scholarly_status']).is_equal_to(expected_profile.scholarly_status)
        assert_that(responsed_profile['created_at']).is_equal_to(reformat_datetime(expected_profile.created_at))
        assert_that(responsed_profile['updated_at']).is_equal_to(reformat_datetime(expected_profile.updated_at))

    @staticmethod
    def _assert_coin_history(response_coin_history, expected_coin_history):
        assert_that(response_coin_history['id']).is_equal_to(expected_coin_history.id)
        assert_that(response_coin_history['profile']).is_equal_to(expected_coin_history.profile.id)
        assert_that(response_coin_history['rest_coin']).is_equal_to(expected_coin_history.rest_coin)
        assert_that(response_coin_history['reason']).is_equal_to(expected_coin_history.reason)
        assert_that(response_coin_history['message']).is_equal_to(expected_coin_history.message)
        assert_that(response_coin_history['created_at']).is_equal_to(
            reformat_datetime(expected_coin_history.created_at))
        assert_that(response_coin_history['updated_at']).is_equal_to(
            reformat_datetime(expected_coin_history.updated_at))

    def test_should_fail_get_jwt_token(self):
        # Given: user, profile, 올바르지 않은 email, password가 주어진다.
        baker.make('users.Profile')

        invalid_payload = {
            'email': 'invalid_email@email.com',
            'password': 'invalid_password',
        }

        # When: login api를 호출한다.
        response = self.client.post('/api/users/tokens/', data=invalid_payload)

        # Then: login에 실패하고, 401 status code가 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_401_UNAUTHORIZED)
        assert_that(response.data['detail']).is_equal_to('No active account found with the given credentials')

    def test_should_refresh_jwt_token(self):
        # Given: user와 user의 refresh token이 주어진다.
        user = baker.make('users.User', is_active=True)
        refresh_token = str(RefreshToken.for_user(user))

        # When: token refresh api를 호출한다.
        payload = {
            'refresh': refresh_token,
        }
        response = self.client.post('/api/users/tokens/refresh/', data=payload)

        # Then: access token이 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that('access' in response.data).is_true()
