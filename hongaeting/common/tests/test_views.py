from assertpy import assert_that
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase


class HealthViewTestCase(APITestCase):

    def test_should_get_health_page(self):
        # Given:

        # When: health page를 요청한다.
        response = self.client.get('/health/')

        # Then: health page가 반환된다.
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response.data['Profile']).is_equal_to(settings.PROFILE)
