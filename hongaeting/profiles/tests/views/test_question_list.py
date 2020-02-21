from inspect import getmembers
from assertpy import assert_that
from rest_framework.test import APITestCase
from profiles.models import QuestionList, QuestionItem

import datetime
import profiles.models


class QuestionListTestCase(APITestCase):
    def test_should_use_question_list_after_specific_time(self):
        # Given: QuestionList가 사용되는지 확인할 prime_time이라는 시간 객체가 하나 주어진다.
        time_to_delete_Question_model = datetime.datetime(2020, 3, 9)

        # When: profiles.models의 member를 확인한다.

        # Then: prime_time 이후에 QuestionList, QuestionItem model이 있으면 테스트를 실패한다.
        members_name_index = 0
        if time_to_delete_Question_model < datetime.datetime.now():
            for tuples in getmembers(profiles.models):
                assert_that(tuples[members_name_index]).is_not_equal_to('QuestionList')
                assert_that(tuples[members_name_index]).is_not_equal_to('QuestionItem')
