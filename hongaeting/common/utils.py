from django.conf import settings
from django.core.mail import EmailMessage


class Email:
    def send_email(self, title, html_content, to_email):
        if settings.TEST:
            # Test 환경에서는 실제로 이메일을 전송할 수 없으므로 메일이 성공적으로 전송됐음을 알리는 1을 반환한다.
            return 1
        mail = EmailMessage(title, html_content, to=to_email)
        mail.content_subtype = 'html'
        return mail.send()


def reformat_datetime(datetime):
    date, time = str(datetime).split(' ')

    return f'{date}T{time.split("+")[0]}Z'
