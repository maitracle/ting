from bs4 import BeautifulSoup
from django.conf import settings

from common.requests import Request


class Kakao:
    # Todo(maitracle): test code 작성
    valid_html_string = ''
    deleted_link_string = 'Link for this open chatroom has been deleted.'

    @classmethod
    def is_valid_kakao_link(cls, kakao_link):
        if settings.TEST:

            return True
        request = Request.instance()

        response = request.get(kakao_link)

        soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')

        for string_tag in soup.find_all('strong'):
            if cls.deleted_link_string in string_tag.contents:
                return False

        return True
