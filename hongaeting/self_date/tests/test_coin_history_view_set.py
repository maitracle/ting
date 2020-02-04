from assertpy import assert_that
from rest_framework import status
from rest_framework.test import APITestCase

from self_date.models import CoinHistory

class CoinHistoryViewSetTestCase(APITestCase):

    def test_should_create_and_load_coin_history(self):
        # Given: coin history 주어진다.
        coin_history_data = {
            'user' : 'test_user',
            'rest_coin' : '2',
            'reason' : 'Signup',
        }

