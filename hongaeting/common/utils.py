from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage


class Email:
    @classmethod
    def send_email(cls, title, html_content, to_email):
        if settings.TEST:
            # Test 환경에서는 실제로 이메일을 전송할 수 없으므로 메일이 성공적으로 전송됐음을 알리는 1을 반환한다.
            return 1

        to_email_list = to_email if isinstance(to_email, list) or isinstance(to_email, tuple) else [to_email]
        mail = EmailMessage(title, html_content, to=to_email_list)
        mail.content_subtype = 'html'

        return mail.send()


def reformat_datetime(datetime_data):
    datetime_data += timedelta(hours=9)
    date, time = str(datetime_data).split(' ')

    return f'{date}T{time.split("+")[0]}+09:00'
