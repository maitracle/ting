import os
from datetime import datetime

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
    date, time = str(datetime_data.split(' ')

    return f'{date}T{time.split("+")[0]}Z'


def set_filename_format(now, instance, original_filename):
    return f"{instance.user.id}-{str(now.date())}-{now.microsecond}{os.path.splitext(original_filename)[1]}"


def user_directory_path(instance, original_filename):
    path = f"profiles/{instance.user.get_full_name()}/{set_filename_format(datetime.now(), instance, original_filename)}"
    return path
