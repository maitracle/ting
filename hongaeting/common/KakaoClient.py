from abc import ABC

from bs4 import BeautifulSoup
from django.conf import settings

from common.exceptions import ExternalRequestTimeoutOrUnreachable
from common.requests import Request


class KakaoClient(ABC):

    @classmethod
    def instance(cls):
        if settings.TEST:
            return KakaoClientWithTest()

        return KakaoClientWithRequest()

    @classmethod
    def is_valid_kakao_link(cls, kakao_link):
        pass


class KakaoClientWithRequest(KakaoClient):
    @classmethod
    def is_valid_kakao_link(cls, kakao_link):
        request = Request.instance()

        try:
            html_text = request.get(kakao_link).text

        except ExternalRequestTimeoutOrUnreachable:
            return False

        soup = BeautifulSoup(html_text.encode('utf8'), 'html.parser')
        found_chat_room_button = soup.find('button', class_='btn_chat')

        return True if found_chat_room_button else False


class KakaoClientWithTest(KakaoClient):
    open_room_kakao_link = 'https://open.kakao.com/o/open_room_link'
    close_room_kakao_link = 'https://open.kakao.com/o/close_room_kakao_link'

    @classmethod
    def is_valid_kakao_link(cls, kakao_link):
        return kakao_link == cls.open_room_kakao_link
