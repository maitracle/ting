import datetime
from assertpy import assert_that
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

class QuestionListTestCase(APITestCase):
    prime_time = datetime.datetime(2020, 3, 9)
    assert_that(datetime.datetime.now()).is_before(prime_time)