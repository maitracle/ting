from assertpy import assert_that
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

from common.constants import REWORD_COUNT, COIN_CHANGE_REASON
from users.models import User


class UserAdminTestCase(APITestCase):

    def setUp(self) -> None:
        self.email = 'staff@email.com'
        self.password = 'staff_password'
        self.user = User.objects.create_superuser(self.email, self.password)

    def test_confirm_user(self):
        # Given: superuser 계정과 confirm_user action data가 주어진다.
        baker.make('users.User', is_staff=False, _quantity=10)
        user_queryset = User.objects.filter(is_staff=False)

        for user in user_queryset:
            baker.make('users.Profile', user=user)

        data = {
            'action': 'confirm_users',
            '_selected_action': user_queryset.values_list('pk', flat=True),
        }

        # When: user_admin의 confirm_users action을 요청한다.
        self.client.login(username=self.email, password=self.password)

        change_url = reverse('admin:users_user_changelist')
        self.client.post(change_url, data)

        # Then: action의 대상이 된 user들의 is_confirmed_student가 True로 수정된다.
        #       학생 인증으로 인한 코인 지급 coin_history가 생성된다.
        changed_user_queryset = User.objects.filter(id__in=data['_selected_action'])
        for user in changed_user_queryset:
            assert_that(user.is_confirmed_student).is_true()

            last_coin_history = user.profile.coin_histories.last()
            assert_that(last_coin_history.rest_coin).is_equal_to(REWORD_COUNT['CONFIRM_USER'])
            assert_that(last_coin_history.reason).is_equal_to(COIN_CHANGE_REASON.CONFIRM_USER)
            assert_that(last_coin_history.message).is_equal_to('')
