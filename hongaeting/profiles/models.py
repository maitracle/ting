from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from model_utils import Choices

from common.constants import UNIVERSITY_LIST
from common.models import BaseModel


class QuestionList(BaseModel):
    name = models.CharField(max_length=30)
    university = models.CharField(max_length=30, choices=UNIVERSITY_LIST)
    season = models.IntegerField()
    version = models.IntegerField()

    def __str__(self):
        return self.name


class QuestionItem(BaseModel):
    name = models.CharField(max_length=100)
    question_list = models.ForeignKey('profiles.QuestionList', on_delete=models.CASCADE)
    question_number = models.PositiveSmallIntegerField()


class Profile(BaseModel):
    MAX_CHARFIELD_LENGTH = 300
    BODY_TYPE_CHOICES = Choices('SKINNY', 'SLIM', 'NORMAL', 'CHUBBY', 'GLAMOROUS', 'FIT')
    GENDER_CHOICES = Choices('MALE', 'FEMALE')
    RELIGION_CHOICES = Choices('NOTHING', 'CHRISTIANITY', 'BUDDHISM', 'CATHOLIC', 'ETC')
    IS_SMOKE_CHOICES = Choices('YES', 'NO', 'SOMETIMES')
    CAMPUS_LOCATION_CHOICES = Choices('SEOUL', 'INTERNATIONAL', 'SINCHON')

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=8, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(19)], null=True)
    height = models.PositiveSmallIntegerField(null=True)
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES, null=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, null=True)
    is_smoke = models.CharField(max_length=10, choices=IS_SMOKE_CHOICES, null=True)
    campus_location = models.CharField(max_length=20, choices=CAMPUS_LOCATION_CHOICES, null=True)

    tag = models.CharField(max_length=100, null=True)
    image = models.CharField(max_length=100, null=True)
    one_sentence = models.CharField(max_length=MAX_CHARFIELD_LENGTH, null=True)

    appearance = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)], null=True)
    personality = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)], null=True)
    hobby = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)], null=True)
    date_style = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)], null=True)
    ideal_type = models.CharField(max_length=MAX_CHARFIELD_LENGTH, validators=[MinLengthValidator(120)], null=True)
    chat_link = models.URLField(null=True)

    is_active = models.BooleanField(default=True)

    def clean(self):
        # Todo: user를 create 할 때 atomic하게 profile도 만들어지는 상황에서 clean이 실행되지 않는 문제를 해결해야 한다.
        if self.user.university == 'HONGIK':
            if not self.campus_location == 'SEOUL':
                raise ValidationError('Not Valid Campus')
        elif self.user.university == 'KYUNGHEE':
            if not (self.campus_location == 'SEOUL' or self.campus_location == 'INTERNATIONAL'):
                raise ValidationError('Not Valid Campus')
        elif self.user.university == 'YONSEI':
            if not (self.campus_location == 'SINCHON' or self.campus_location == 'INTERNATIONAL'):
                raise ValidationError('Not Valid Campus')
        if 'kakao' not in self.chat_link:
            raise ValidationError('Not Valid chat link')
