from django.core.exceptions import ValidationError


def chat_link_validator(value):
    if not 'kakao' in value:
        raise ValidationError('Not Valid chat link')
    else:
        return value