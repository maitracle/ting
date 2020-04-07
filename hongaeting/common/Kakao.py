from abc import ABC

from bs4 import BeautifulSoup
from django.conf import settings

from common.requests import Request


class Kakao(ABC):
    # Todo(maitracle): test code 작성
    valid_html_string = ''
    deleted_link_string = 'Link for this open chatroom has been deleted.'

    @classmethod
    def instance(cls):
        if settings.TEST:
            return KakaoWithTest()

        return KakaoWithRequest()

    @classmethod
    def is_valid_kakao_link(cls, kakao_link):
        pass


class KakaoWithRequest(Kakao):

    @classmethod
    def is_valid_kakao_link(cls, kakao_link):
        request = Request.instance()

        try:
            html_text = request.get(kakao_link).text

        except AttributeError:
            return False

        soup = BeautifulSoup(html_text.encode('utf8'), 'html.parser')

        for string_tag in soup.find_all('strong'):
            if cls.deleted_link_string in string_tag.contents:
                return False

        return True


class KakaoWithTest(Kakao):
    valid_kakao_link = 'https://open.kakao.com/o/valid_link'
    invalid_kakao_link = 'https://open.kakao.com/o/invalid_link'

    @classmethod
    def is_valid_kakao_link(cls, kakao_link):
        return kakao_link == cls.valid_kakao_link
