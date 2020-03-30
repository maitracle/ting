import os

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from model_utils import Choices

from common.Kakao import Kakao
from common.models import BaseModel
from common.models import BaseModel
from common.models import BaseModel
from users.models import User


def image_path(instance, original_filename):
    path = f'profiles/{instance.profile.user.get_full_name()}/image{os.path.splitext(original_filename)[1]}'
    return path


def chat_link_validator(value):
    print(value)
    if not 'kakao' in value:
        raise ValidationError('Not Valid chat link')
    else:
        return value


class SelfDateProfile(BaseModel):
    BODY_TYPE_CHOICES = Choices('SKINNY', 'SLIM', 'SLIM_TONED', 'NORMAL', 'BUFF', 'CHUBBY')
    RELIGION_CHOICES = Choices('NOTHING', 'CHRISTIANITY', 'BUDDHISM', 'CATHOLIC', 'ETC')
    IS_SMOKE_CHOICES = Choices('YES', 'NO')

    profile = models.OneToOneField('users.Profile', on_delete=models.CASCADE)

    nickname = models.CharField(max_length=8, unique=True)
    height = models.PositiveSmallIntegerField(null=True)
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES, blank=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True)
    is_smoke = models.CharField(max_length=10, choices=IS_SMOKE_CHOICES, blank=True)

    tags = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to=image_path, blank=True, null=True, max_length=1000)
    one_sentence = models.CharField(max_length=35, blank=True)

    appearance = models.CharField(max_length=1000, validators=[MinLengthValidator(120)], blank=True)
    personality = models.CharField(max_length=1000, validators=[MinLengthValidator(120)], blank=True)
    hobby = models.CharField(max_length=1000, validators=[MinLengthValidator(120)], blank=True)
    date_style = models.CharField(max_length=1000, validators=[MinLengthValidator(60)], blank=True)
    ideal_type = models.CharField(max_length=1000, validators=[MinLengthValidator(120)], blank=True)
    chat_link = models.URLField(blank=True, validators=[chat_link_validator])

    is_active = models.BooleanField(default=True)

    # def clean(self):
    # Todo(10000001a): user를 create 할 때 atomic하게 profile도 만들어지는 상황에서 clean이 실행되지 않는 문제를 해결해야 한다.
    # if self.user.university == 'HONGIK':
    #     if not self.campus_location == 'SEOUL':
    #         raise ValidationError('Not Valid Campus')
    # elif self.user.university == 'KYUNGHEE':
    #     if not (self.campus_location == 'SEOUL' or self.campus_location == 'INTERNATIONAL'):
    #         raise ValidationError('Not Valid Campus')
    # elif self.user.university == 'YONSEI':
    #     if not (self.campus_location == 'SINCHON' or self.campus_location == 'INTERNATIONAL'):
    #         raise ValidationError('Not Valid Campus')

    @property
    def is_valid_chat_link(self):
        try:
            is_valid = Kakao.is_valid_kakao_link(self.chat_link)
        except:
            is_valid = False
        return is_valid


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_user = models.ForeignKey(User, related_name='liked_user', on_delete=models.CASCADE)
