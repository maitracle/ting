from inspect import getmembers
from assertpy import assert_that
from rest_framework.test import APITestCase
from profiles.models import QuestionList

import datetime
import profiles.models


class QuestionListTestCase(APITestCase):
    def test_should_use_question_list_after_specific_time(self):
        # Given: QuestionList가 사용되는지 확인할 prime_time이라는 시간 객체가 하나 주어진다.
        prime_time = datetime.datetime(2020, 3, 9)

        # When: prime_time을 지났을 때 QuestionList가 존재한다.
        if prime_time < datetime.datetime.now():

            # Then: 에러가 발생한다.
            for tuples in getmembers(profiles.models):
                assert_that(tuples[0]).is_not_equal_to('QuestionList')
